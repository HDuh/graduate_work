from uuid import UUID

from .base_schema_mixin import BaseMixin

__all__ = (
    'OrderSchema',
)


class OrderSchema(BaseMixin):
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
