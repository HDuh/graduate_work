from .base import BaseSchema

__all__ = (
    'OrderSchema',
)


class OrderSchema(BaseSchema):
    customer_id: str
    price_id: str
    quantity: int
