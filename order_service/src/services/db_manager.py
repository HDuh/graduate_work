from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import OrderStatus
from src.db.base import get_session

__all__ = (
    'get_db_manager',
    'DbManager',
    # 'get_auth_manager'
)

from src.db.models import User, Order, Product


class DbManager:
    def __init__(self, session):
        self.session = session

    async def get_by_id(self, model, idx):
        result = await self.session.execute(
            select(model)
            .where(model.id == idx)
        )
        if result := result.scalars().first():
            return result

        return

    async def get_all(self, model):
        result = await self.session.execute(
            select(model)
            .order_by(
                model.id
            )
        )
        return result.scalars().all()

    async def add(self, model_instance):
        self.session.add(model_instance)

    async def remove(self, model, idx):
        result = await self.session.execute(
            select(model)
            .where(model.id == idx)
        )
        self.session.delete(result)
        return result

    async def get_user_id_by_customer_id(self, customer_id):
        result = await self.session.execute(
            select(User)
            .where(User.customer_id == customer_id)
        )
        if result := result.scalars().first():
            return result

    async def update_order(self, user_id, pay_intent_id):
        first_order = await self.session.execute(
            select(Order)
            .where(Order.user_id == user_id and Order.status == OrderStatus.UNPAID)
            .limit(1)
        )
        order_id_for_update = first_order.scalars().first().to_dict()['id']
        result = await self.session.execute(
            update(Order)
            .where(Order.id == order_id_for_update)
            .values(status=OrderStatus.PAID, pay_intent_id=pay_intent_id)
            .execution_options(synchronize_session="fetch")
        )

        if result := result.scalars().first():
            return result

    async def delete_unpaid_orders(self, user_id):
        result = await self.session.execute(
            delete(Order)
            .where(
                Order.user_id == user_id
                and Order.status == OrderStatus.UNPAID)
            .execution_options(synchronize_session="fetch")
        )
        return result

    async def get_product_by_product_stripe_id(self, product_stripe_id):
        result = await self.session.execute(
            select(Product)
            .where(Product.product_stripe_id == product_stripe_id)
        )
        if result := result.scalars().first():
            return result



# class AuthManager:
#     @classmethod
#     async def async_get_user_info(cls, user_id: str):
#         # тут должен быть запрос в сервис авторизации для получения данных пользователя
#         return

@lru_cache()
def get_db_manager(session: AsyncSession = Depends(get_session)) -> DbManager:
    return DbManager(session)

# async def get_auth_manager():
#     return AuthManager
