from sqlalchemy import update
from sqlalchemy.future import select

from src.db.base import get_session
from src.db.models import User
from src.services import StripeManager

__all__ = (
    'DbManager',
)


class DbManager:
    __session = get_session

    @classmethod
    async def async_get_by_id(cls, model, idx):
        """
        Получение данных из БД по id
        """
        async with cls.__session() as session:
            result = await session.execute(select(model).where(model.id == idx))
            return result.scalar()

    @classmethod
    async def async_get_by_name(cls, model, name):
        """
        Получение данных из БД по name
        """
        async with cls.__session() as session:
            result = await session.execute(select(model).where(model.name == name))
            return result.scalar()

    @classmethod
    async def async_get_all(cls, model):
        """
        Получение всех данных из модели
        """
        async with cls.__session() as session:
            result = await session.execute(select(model))
            return result.scalars().all()

    @classmethod
    async def async_save(cls, model):
        """
        Сохранить модель в БД
        """
        async with cls.__session() as session:
            session.add(model)

    @classmethod
    async def async_delete(cls, model):
        """
        Удалить модель из БД
        """
        async with cls.__session() as session:
            await session.delete(model)

    @classmethod
    async def async_update(cls, model, **kwargs):
        """
        Обновить данные модели в БД
        """
        async with cls.__session() as session:
            await session.execute(
                update(model.__class__)
                .where(model.__class__.id == model.id)
                .values(kwargs)
            )

    @classmethod
    async def async_get_or_create_user(cls, user_id):
        """
        Проверка наличия/создание пользователя в БД
        """
        if not (user := await cls.async_get_by_id(User, user_id)):
            user = User(id=user_id, customer_id=StripeManager.create_customer().stripe_id)
            await cls.async_save(user)
        return user
