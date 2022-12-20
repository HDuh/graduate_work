from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.models import Subscription
from src.db.base import get_session

__all__ = (
    'get_db_manager',
    'DbManager'
)


class DbManager:

    async def session(self) -> AsyncSession:
        return get_session()

    # @classmethod
    async def async_get_by_id(self, model, idx):
        session = await self.session()
        result = session.execute(select(model).where(model.id == idx))
        return result.scalar()

    # @classmethod
    async def async_save(self, model):
        self.session.add(model)
        await self.session.commit()

    # @classmethod
    async def async_get_user_subscription(self, user_id):
        result = await self.session.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        return result.scalar()


async def get_db_manager():
    return DbManager()
