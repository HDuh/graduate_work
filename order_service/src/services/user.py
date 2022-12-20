from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_session
from src.db.models import Product, User, Order, Subscription
from .base_db_service import BaseDBService
from ..core import OrderStatus, SubscriptionStatus
from ..schemas.subscriptions import SubscriptionCreate


class UserService(BaseDBService):

    async def check_user_orders(self, product_id, user_id):
        stm = (
            select(Order)
            .join(Order.product)
            .where(
                Product.id == product_id,
                Order.user_id == user_id,
                Order.status == OrderStatus.UNPAID
            )
        )

        res = await self.session.execute(stm)
        return res.one_or_none()

    async def check_user_subscriptions(self, user_id):
        stm = (
            select(Subscription)
            .where(
                Subscription.status != SubscriptionStatus.CANCELLED,
                Subscription.user_id == user_id
            )
        )
        res = await self.session.execute(stm)

        return res.one_or_none()

    async def get_by_customer_id(self, customer_id):
        result = await self.session.execute(
            select(self.model)
            .where(self.model.customer_id == customer_id)
        )

        result = result.one_or_none()
        if result:
            return result[0]
        return

    async def get_active_subscription(self, user_id):
        result = await self.session.execute(
            select(Subscription)
            .where(
                Subscription.user_id == user_id,
                Subscription.status == SubscriptionStatus.ACTIVE)
        )
        result = result.one_or_none()

        if result:
            return result[0]
        return

    async def update_subscription(self, user_id, status):
        subscription = await self.get_active_subscription(user_id)
        sub_id = subscription.to_dict()["id"]

        await self.session.execute(
            update(Subscription)
            .where(Subscription.id == sub_id)
            .values(status=status)
            .execution_options(synchronize_session="fetch")
        )

    async def create_subscription(self, user_id, start, end, product_id, status=SubscriptionStatus.ACTIVE):
        subscription_db = Subscription(
            user_id=user_id,
            status=status,
            start_date=start,
            end_date=end,
            product_id=product_id)

        await self.add(subscription_db)

        return SubscriptionCreate(**subscription_db.to_dict())


@lru_cache()
def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session, User)
