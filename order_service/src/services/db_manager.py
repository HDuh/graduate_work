from sqlalchemy.future import select

from src.db.base import get_session
from src.db.models import Subscription, User
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
    async def async_save(cls, model):
        """
        Сохранить модель в БД
        """
        async with cls.__session() as session:
            session.add(model)

    @classmethod
    async def async_get_user_subscription(cls, user_id):
        """
        Получить подписки пользователя по id
        """
        async with cls.__session() as session:
            result = await session.execute(
                select(Subscription).where(Subscription.user_id == user_id)
            )
            return result.scalar()

    @classmethod
    async def async_check_or_create_user(cls, user_id):
        """
        Проверка наличия/создание пользователя в БД
        """
        if not (user := await cls.async_get_by_id(User, user_id)):
            user = User(id=user_id, customer_id=StripeManager.create_customer().stripe_id)
            await cls.async_save(user)
        return user
