from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from db.models import Customer
from services.payment_systems.stripe_service import AbstractPaymentSystem
from services.payment_systems.stripe_service import get_payment_system


class CustomerService:
    def __init__(self, provider: AbstractPaymentSystem, session: AsyncSession):
        self.provider = provider
        self.session = session

    async def get_customer(self, user_id) -> str:
        result = await self.session.execute(
            select(
                Customer.id, Customer.provider_customer_id)
            .where(Customer.user_id == user_id)
        )
        result = result.first()

        if not result:
            result = await self.create_customer(user_id)

        return result

    async def create_customer(self, user_id):
        provider_customer = await self.provider.create_customer()
        customer = Customer(
            user_id=user_id,
            provider_customer_id=provider_customer.id,
        )

        await self.session.execute(customer)

        return customer


@lru_cache()
def get_customer_service(
        session: AsyncSession = Depends(get_session),
        provider: AbstractPaymentSystem = Depends(get_payment_system)
):
    return CustomerService(
        session=session,
        provider=provider,
    )
