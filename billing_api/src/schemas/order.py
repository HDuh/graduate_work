from .base import BaseSchema


class OrderSchema(BaseSchema):
    customer_id: str
    price_id: str
    quantity: int
