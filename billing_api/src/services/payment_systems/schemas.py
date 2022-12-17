from pydantic import BaseModel

from schemas.base import BaseSchema


class ProviderBase(BaseSchema):
    amount: int
    customer: str
    currency: str = "RUB"


class ProviderPayment(ProviderBase):
    setup_future_usage: str = 'off_session'
    confirm: bool = False


class ProviderPaymentCancel(ProviderBase):
    payment: str


class ProviderPaymentResult(BaseSchema):
    id: str
    client_secret: str


class CheckoutInfo(BaseModel):
    checkout_url: str
    checkout_id: str
