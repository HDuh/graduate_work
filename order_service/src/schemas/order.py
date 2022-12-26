from uuid import UUID

from pydantic import Field

from src.schemas.base import BaseMixin


class RefundCreate(BaseMixin):
    user_id: UUID
    product_id: UUID


class RefundComplete(BaseMixin):
    user_id: UUID
    amount: int
    product: str


class OrderCreate(BaseMixin):
    user_id: UUID
    order_id: UUID
    payment_id: str = Field(default='')
    customer_id: str
    price_id: str
    quantity: int
    service_name: str


class OrderForBilling(BaseMixin):
    product_id: UUID
