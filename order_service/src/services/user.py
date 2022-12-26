import logging
from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import OrderStatus, SubscriptionStatus
from src.db.base import get_session
from src.db.models import Product, User, Order, Subscription
from src.schemas.subscriptions import Create
from src.services import StripeManager
from .base_db_service import BaseDBService

logger = logging.getLogger(__name__)


class UserService(BaseDBService):

    async def last_unpaid_user_order(self, product_id, user_id):
        stm = (
            select(Order)
            .join(Order.product)
            .where(
                Product.id == product_id,
                Order.user_id == user_id,
                Order.status == OrderStatus.UNPAID
            )
            .order_by(desc(Order.created_at))
        )

        res = await self.session.execute(stm)

        return res.scalars().first()

    async def last_user_order(self, product_id, user_id):
        stm = (
            select(Order)
            .join(Order.product)
            .where(
                Product.id == product_id,
                Order.user_id == user_id,
            )
            .order_by(desc(Order.created_at))
        )

        result = await self.session.execute(stm)
        result = result.scalars()
        if result:
            return result.first()

    async def last_paid_user_order(self, product_id, user_id):
        stm = (
            select(Order)
            .join(Order.product)
            .where(
                Product.id == product_id,
                Order.user_id == user_id,
                Order.status == OrderStatus.PAID
            )
            .order_by(desc(Order.created_at))
        )

        result = await self.session.execute(stm)
        return result.scalars().first()

    async def get_by_customer_id(self, customer_id):
        result = await self.session.execute(
            select(self.model)
            .where(self.model.customer_id == customer_id)
        )
        return result.scalar()

    async def active_subscription(self, user_id):
        result = await self.session.execute(
            select(Subscription)
            .where(
                Subscription.user_id == user_id,
                Subscription.status == SubscriptionStatus.ACTIVE
            )
        )
        return result.scalar()

    async def not_cancelled_subscription(self, user_id):
        result = await self.session.execute(
            select(Subscription)
            .where(
                Subscription.status != SubscriptionStatus.CANCELLED,
                Subscription.user_id == user_id
            )
        )
        return result.scalar()

    async def cancel_subscription(self, user_id):
        if subscription := await self.not_cancelled_subscription(user_id):
            await self.session.execute(
                update(subscription.__class__)
                .where(subscription.__class__.id == subscription.id)
                .values(status=SubscriptionStatus.CANCELLED)
                .execution_options(synchronize_session="fetch")
            )
            logger.info(f'Subscription [%s] canceled.', subscription.id)

    async def update_subscription(self, user_id, status):
        if subscription := await self.active_subscription(user_id):
            await self.session.execute(
                update(subscription.__class__)
                .where(subscription.__class__.id == subscription.id)
                .values(status=status)
                .execution_options(synchronize_session="fetch")
            )
            logger.info(f'Subscription [%s] updated.', subscription.id)
            return subscription

    async def create_subscription(self, user_id, start,
                                  end, product_id, subscription_id,
                                  status=SubscriptionStatus.ACTIVE):
        subscription_db = Subscription(
            user_id=user_id,
            status=status,
            start_date=start,
            end_date=end,
            product_id=product_id)

        if not await self.not_cancelled_subscription(user_id):
            order = await self.last_user_order(product_id, user_id)
            await self.add(subscription_db)
            StripeManager.add_to_metadata(subscription_id, user_id, order.id)

            logger.info(f'Subscription for user [%s] added to DB.', user_id)
            return Create.from_orm(subscription_db)

    async def deactivate_subscription(self, user_id):
        user = await self.get_by_id(user_id)
        if user.subscription.filter_by(status=SubscriptionStatus.ACTIVE):
            StripeManager.deactivate_subscription(user_id)

            result = await self.update_subscription(user_id, SubscriptionStatus.INACTIVE)
            logger.info(f'Subscription for user [%s] deactivated.', user_id)
            return result


@lru_cache()
def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session, User)
