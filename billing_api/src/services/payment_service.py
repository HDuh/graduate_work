from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

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


async def get_payment_service(session: AsyncSession = Depends(get_session)) -> PaymentService:
    return PaymentService(session, Payment)
