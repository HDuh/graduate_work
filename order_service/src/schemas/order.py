from src.schemas.base import BaseSchema


class OrderCreate(BaseSchema):
    customer_id: str
    price_id: str
    quantity: int
