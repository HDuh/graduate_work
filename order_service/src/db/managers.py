from functools import lru_cache

from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import row

from .base import get_session
from src.db.models import User

__all__ = (
    'get_db_manager',
    # 'get_auth_manager'
)


class DbManager:

    @classmethod
    async def async_get_user(cls, user_id):
        async with get_session() as session:
            return await session.execute(
                select(User)
                .where(User.id == user_id)
            )


# class AuthManager:
#     @classmethod
#     async def async_get_user_info(cls, user_id: str):
#         # тут должен быть запрос в сервис авторизации для получения данных пользователя
#         return

@lru_cache
async def get_db_manager():
    return DbManager


# async def get_auth_manager():
#     return AuthManager
