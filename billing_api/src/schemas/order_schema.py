from uuid import UUID

from pydantic import BaseModel

__all__ = (
    'OrderSchema',
)


class OrderSchema(BaseModel):
    user_id: UUID
    order_id: UUID
    customer_id: str
    price_id: str
    quantity: int
    service_name: str

    def to_payment_schema(self):
        return {
            attr: value
            for attr, value in self.__dict__.items()
            if attr != 'quantity'
        }

    class Config:
        orm_mode = True
