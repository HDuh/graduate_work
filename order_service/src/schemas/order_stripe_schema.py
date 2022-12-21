from pydantic import BaseModel

__all__ = (
    'OrderSchema',
)


class OrderSchema(BaseModel):
    customer_id: str
    price_id: str
    quantity: int
