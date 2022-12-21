from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import OrderStatus
from src.db.base import get_session
from src.db.models import User, Order, Product
from src.schemas.order import OrderCreate
from src.services import StripeManager
from .base_db_service import BaseDBService
from .product import ProductService, get_product_service
from .user import UserService, get_user_service


class OrderService(BaseDBService):
    def __init__(self, session, model, user_service, product_service):
        super(OrderService, self).__init__(session, model)
        self.user_service: UserService = user_service
        self.product_service: ProductService = product_service

    async def create_order(self, product_id, user_id):
        if not (user := await self.user_service.get_by_id(user_id)):
            customer = StripeManager.create_customer()
            user = User(id=user_id, customer_id=customer['id'])
            await self.add(user)

        check_orders = await self.user_service.check_unpaid_user_orders(product_id, user_id)
        check_subscriptions = await self.user_service.not_cancelled_subscription(user_id)

        if not check_orders and not check_subscriptions:
            product = await self.product_service.get_by_id(product_id)
            new_order = Order(
                user_id=user.id,
                status=OrderStatus.UNPAID,
            )

            new_order.product.append(product)
            await self.add(new_order)

            return OrderCreate(
                customer_id=user.customer_id,
                price_id=product.price_stripe_id,
                quantity=1)

    async def update_order(self, user_id, pay_intent_id=None, status=OrderStatus.PAID):

        status_to_search = OrderStatus.PAID

        if status == OrderStatus.PAID:
            status_to_search = OrderStatus.UNPAID

        result = await self.session.execute(
            select(Order)
            .where(
                Order.user_id == user_id,
                Order.status == status_to_search)
        )
        order_obj = result.scalars().first().to_dict()

        if not pay_intent_id:
            pay_intent_id = order_obj['pay_intent_id']

        order_id_for_update = order_obj['id']
        print(f"ORDER ID FOR UPDATE: {order_id_for_update}")

        await self.session.execute(
            update(Order)
            .where(Order.id == order_id_for_update)
            .values(status=status, pay_intent_id=pay_intent_id)
            .execution_options(synchronize_session="fetch")
        )

    async def delete_unpaid_orders(self, user_id):
        result = await self.session.execute(
            delete(Order)
            .where(
                Order.user_id == user_id
                and Order.status == OrderStatus.UNPAID)
            .execution_options(synchronize_session="fetch")
        )
        return result

    async def create_refund(self, user_id, product_id):

        order: Order = await self.user_service.last_paid_user_order(product_id, user_id)
        if not order:
            return
        product: Product = await self.product_service.get_by_id(product_id)

        amount = product.price
        pay_intent_id = order.pay_intent_id

        # Refund to stripe
        StripeManager.refund(amount, pay_intent_id)

        # Cancel subscription to stripe
        StripeManager.cancel_subscription(user_id)

        await self.update_order(user_id, status=OrderStatus.CANCELED)

        amount = amount

        return {'amount': amount, 'user_id': user_id, 'product': product.name}



@lru_cache()
def get_order_service(
        session: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        product_service: ProductService = Depends(get_product_service)
) -> OrderService:
    return OrderService(session, Order, user_service, product_service)
