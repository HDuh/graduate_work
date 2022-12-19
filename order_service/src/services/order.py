from functools import lru_cache

from fastapi import Depends

from src.core import SubscriptionStatus, OrderStatus
from src.db.models import Product, User, Order
from src.schemas.order import OrderCreate
from src.services import get_db_manager, DbManager, StripeManager


class OrderService:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    async def create_order(self, product_id, user_id):
        if not (user := await self.db_manager.get_by_id(User, user_id)):
            customer = StripeManager.create_customer()
            user = User(id=user_id, customer_id=customer['id'])
            await self.db_manager.add(user)

        if not user.subscription or user.subscription.status == SubscriptionStatus.INACTIVE:
            # TODO: нужна проверка для ограничения создания нескольких UNPAID заказов на один продукт для Юзера
            # if not any([i.product.id == product_id for i in user.order if i.status == OrderStatus.UNPAID]):
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
