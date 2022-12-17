import abc
from typing import Optional

from db.models import Payment

from schemas.customer import CustomerSchema
from .schemas import CheckoutInfo, ProviderPayment, ProviderPaymentResult


# TODO:
#  - mode: 'payment','subscription'
#  - payment_method_types: ['card']


class AbstractPaymentSystem(abc.ABC):

    @abc.abstractmethod
    async def create_checkout(
            self,
            payment: Payment,
            success_url: Optional[str] = None,
            cancel_url: Optional[str] = None,
    ) -> CheckoutInfo:
        ...

    @abc.abstractmethod
    async def create_customer(self) -> CustomerSchema:
        ...

    @abc.abstractmethod
    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        ...
