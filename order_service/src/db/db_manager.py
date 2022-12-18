from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import get_session

__all__ = (
    'get_db_manager',
    'DbManager',
    # 'get_auth_manager'
)


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

        return None

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


# class AuthManager:
#     @classmethod
#     async def async_get_user_info(cls, user_id: str):
#         # тут должен быть запрос в сервис авторизации для получения данных пользователя
#         return
@lru_cache
async def get_db_manager(session: AsyncSession = Depends(get_session)) -> DbManager:
    return DbManager(session)

# async def get_auth_manager():
#     return AuthManager
