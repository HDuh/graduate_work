from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import SubscriptionStatus, OrderStatus
from src.db.models import Product, User, Order
from src.schemas.order import OrderCreate
from src.services import get_db_manager, DbManager, StripeManager


class OrderService:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    async def get_user_instance(self, user_id: UUID):
        if not (user := await self.db_manager.get_by_id(User, user_id)):
            customer = StripeManager.create_customer()
            user = User(id=user_id, customer_id=customer['id'])
            await self.db_manager.add(user)
        return user

    async def confirm_purchase_option(self, user: User, product_id: UUID):
        unpaid_same_product = any(
            order.status == OrderStatus.UNPAID
            for order in user.order
            for product in order.product
            if product.id == product_id
        )
        if (
                (not user.subscription or user.subscription.status == SubscriptionStatus.INACTIVE) and
                not unpaid_same_product
        ):
            return False
        return True

    async def create_order(self, product_id, user_id):
        user = await self.get_user_instance(user_id)
        if not await self.confirm_purchase_option(user, product_id):
            return
        if not user.subscription or user.subscription.status == SubscriptionStatus.INACTIVE:
            if any(
                    (
                            product.id
                            for order in user.order
                            for product in order.product
                            if order.status == OrderStatus.UNPAID and product.id == product_id
                    )
            ):
                return

            product = await self.db_manager.get_by_id(Product, product_id)
            new_order = Order(
                user_id=user.id,
                status=OrderStatus.UNPAID,
            )

            new_order.product.append(product)
            await self.db_manager.add(new_order)

            return OrderCreate(
                customer_id=user.customer_id,
                price_id=product.price_stripe_id,
                quantity=1
            )

    async def get_user_id_by_customer_id(self, customer_id):
        return await self.db_manager.get_user_id_by_customer_id(customer_id)

    async def update_order(self, user_id, pay_intent_id):
        return await self.db_manager.update_order(user_id, pay_intent_id)

    async def delete_unpaid_orders(self, user_id, new_pay_intent_id):
        return await self.db_manager.delete_unpaid_orders(user_id, new_pay_intent_id)


@lru_cache()
def get_order_service(db_manager: DbManager = Depends(get_db_manager)) -> OrderService:
    return OrderService(db_manager)
