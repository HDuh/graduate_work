from functools import lru_cache

from fastapi import Depends

from src.core import SubscriptionStatus
from src.db.models import Subscription
from src.schemas.subscriptions import SubscriptionCreate
from src.services import get_db_manager, DbManager


class SubscriptionService:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    async def create_subscription(self, user_id, start, end, product_id, status=SubscriptionStatus.ACTIVE):
        subscription_db = Subscription(
            user_id=user_id,
            status=status,
            start_date=start,
            end_date=end,
            product_id=product_id)

        await self.db_manager.add(subscription_db)

        return SubscriptionCreate(**subscription_db.to_dict())


@lru_cache()
def get_subscription_service(db_manager: DbManager = Depends(get_db_manager)) -> SubscriptionService:
    return SubscriptionService(db_manager)
