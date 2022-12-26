import logging
from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import OrderStatus
from src.db.base import get_session
from src.db.models import User, Order
from src.schemas.order import OrderCreate
from src.services import StripeManager
from .base_db_service import BaseDBService
from .product import ProductService, get_product_service
from .user import UserService, get_user_service

logger = logging.getLogger(__name__)


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

        check_orders = await self.user_service.last_unpaid_user_order(product_id, user_id)
        check_subscriptions = await self.user_service.not_cancelled_subscription(user_id)

        if check_orders:
            logger.warning('User [%s] has UNPAID order.', user_id)
            return

        if check_subscriptions:
            logger.warning('User [%s] already has subscription.', user_id)
            return

        if not (product := await self.product_service.get_by_id(product_id)):
            return

        new_order = Order(
            user_id=user.id,
            status=OrderStatus.UNPAID,
        )
        new_order.product.append(product)
        await self.add(new_order)
        return OrderCreate(
            user_id=user.id,
            order_id=new_order.id,
            customer_id=user.customer_id,
            price_id=product.price_stripe_id,
            quantity=1,
            service_name='order_service'
        )

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
        order = result.scalars().first()
        pay_intent_id = order.pay_intent_id if not pay_intent_id else pay_intent_id

        await self.session.execute(
            update(Order)
            .where(Order.id == order.id)
            .values(status=status, pay_intent_id=pay_intent_id)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.commit()
        logger.info(f'Order [%s] was updated. Status [%s]', order.id, status)

    async def create_refund(self, user_id, product_id) -> dict | None:
        if not (order := await self.user_service.last_paid_user_order(product_id, user_id)):
            return
        product = await self.product_service.get_by_id(product_id)

        # Refund to stripe
        StripeManager.refund(product.price, order.pay_intent_id, order.id)
        # Cancel subscription to stripe
        StripeManager.cancel_subscription(user_id)
        await self.update_order(user_id, status=OrderStatus.CANCELED)
        logger.info(f'Refund. amount [%d], user [%s], product [%s]', product.price, user_id, product.name)
        return {'amount': product.price, 'user_id': user_id, 'product': product.name}

    async def set_payment_id(self, order_id, **kwargs):
        await self.session.execute(
            update(Order)
            .where(self.model.id == order_id)
            .values(**kwargs)
        )


@lru_cache()
def get_order_service(
        session: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        product_service: ProductService = Depends(get_product_service)
) -> OrderService:
    return OrderService(session, Order, user_service, product_service)
