from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.base import get_session
from src.db.models import Subscription
from contextlib import asynccontextmanager

__all__ = (
    'get_db_manager',
    'DbManager'
)


class DbManager:
    __session = get_session

    @classmethod
    async def async_get_by_id(cls, model, idx):
        async with cls.__session() as session:
            result = await session.execute(select(model).where(model.id == idx))
            return result.scalar()

    @classmethod
    async def async_save(cls, model):
        async with cls.__session() as session:
            session.add(model)

    @classmethod
    async def async_get_user_subscription(cls, user_id):
        async with cls.__session() as session:
            result = await session.execute(
                select(Subscription).where(Subscription.user_id == user_id)
            )
            return result.scalar()


async def get_db_manager():
    return DbManager()
