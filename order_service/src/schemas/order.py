from uuid import UUID

from src.schemas.base import BaseSchema


class OrderRefundCreate(BaseSchema):
    user_id: UUID
    product_id: UUID


class OrderRefundComplete(BaseSchema):
    user_id: UUID
    amount: int
    product: str


class OrderCreate(BaseSchema):
    customer_id: str
    price_id: str
    quantity: int
