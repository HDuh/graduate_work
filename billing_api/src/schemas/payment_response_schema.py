from datetime import datetime
from uuid import UUID

from .base_schema_mixin import BaseMixin

__all__ = (
    'PaymentShortSchema',
    'PaymentFullSchema',
)


class PaymentShortSchema(BaseMixin):
    id: UUID
    user_id: UUID
    order_id: UUID
    status: str
    service_name: str
    created_at: datetime


class PaymentFullSchema(BaseMixin):
    id: UUID
    user_id: UUID
    order_id: UUID
    customer_id: str
    price_id: str
    status: str
    service_name: str
    created_at: datetime
    updated_at: datetime
