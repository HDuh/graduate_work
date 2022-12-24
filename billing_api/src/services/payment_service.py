from datetime import datetime

from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core import PaymentState
from src.db.base import get_session
from src.db.models import Payment
from .base_db_service import BaseDBService

__all__ = (
    'PaymentService',
    'get_payment_service',
)


class PaymentService(BaseDBService):

    async def async_build_and_create(self, order):
        model = self.model(
                **order.to_payment_schema(),
                status=PaymentState.UNPAID
        )
        await self.save(model)

    async def async_payment_update(self, status, **kwargs,):
        print(status)
        print(kwargs)
        await self.session.execute(
            update(self.model).filter_by(**kwargs).values(
                **{'status': status, 'updated_at': datetime.utcnow()}
            )
        )
        await self.session.commit()
        return f'Successfully updated. Order: {kwargs.get("order_id")}'


async def get_payment_service(session: AsyncSession = Depends(get_session)) -> PaymentService:
    return PaymentService(session, Payment)
