from uuid import UUID

from src.schemas.base import BaseSchema


class RefundCreate(BaseSchema):
    user_id: UUID
    product_id: UUID


class RefundComplete(BaseSchema):
    user_id: UUID
    amount: int
    product: str


class OrderCreate(BaseSchema):
    customer_id: str
    price_id: str
    quantity: int
