from datetime import datetime

from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import PaymentState
from src.db.base import get_session
from src.db.models import Payment
from src.schemas import OrderSchema
from .base_db_service import BaseDBService

__all__ = (
    'PaymentService',
    'get_payment_service',
)


class PaymentService(BaseDBService):

    async def async_build_and_create(self, order_schema: OrderSchema):
        """
        Создание и сохранение модели платежа в БД
        """
        model = self.model(
            **order_schema.to_payment_schema(),
            status=PaymentState.UNPAID
        )
        await self.save(model)

    async def async_payment_update(self, status: str, **kwargs) -> str:
        """
        Обновление статуса и времени у модели платежа
        """
        await self.session.execute(
            update(self.model).filter_by(**kwargs).values(
                **{'status': status, 'updated_at': datetime.utcnow()}
            )
        )
        await self.session.commit()
        print(f'Successfully updated. Order: {kwargs.get("order_id")}')
        return f'Successfully updated. Order: {kwargs.get("order_id")}'


async def get_payment_service(session: AsyncSession = Depends(get_session)) -> PaymentService:
    return PaymentService(session, Payment)
