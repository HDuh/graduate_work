from pydantic import BaseModel


class OrderSchema(BaseModel):
    customer_id: str
    price_id: str
    quantity: int
