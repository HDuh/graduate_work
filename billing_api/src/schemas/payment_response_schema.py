from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

__all__ = (
    'PaymentShortSchema',
    'PaymentFullSchema',
)


class PaymentShortSchema(BaseModel):
    id: UUID
    user_id: UUID
    order_id: UUID
    status: str
    service_name: str
    created_at: datetime


class PaymentFullSchema(BaseModel):
    id: UUID
    user_id: UUID
    order_id: UUID
    customer_id: str
    price_id: str
    status: str
    service_name: str
    created_at: datetime
    updated_at: datetime
