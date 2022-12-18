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
    async def async_get_info_by_id(cls, model, idx):
        async with get_session() as session:
            result = await session.execute(
                select(model)
                .where(model.id == idx)
            )
            return result.first()[0]

    @classmethod
    async def async_add_object(cls, model_instance):
        async with get_session() as session:
            await session.execute(
                insert(model_instance)  # класс инстанса сюда
                .values(**model_instance.dict())
                .on_conflict_do_nothing()
            )


# class AuthManager:
#     @classmethod
#     async def async_get_user_info(cls, user_id: str):
#         # тут должен быть запрос в сервис авторизации для получения данных пользователя
#         return

async def get_db_manager():
    return DbManager

# async def get_auth_manager():
#     return AuthManager
