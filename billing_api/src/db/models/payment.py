from datetime import datetime

from sqlalchemy import Column, Enum, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.core import PaymentState
from src.db.models import BaseModel

__all__ = (
    'Payment',
)


class Payment(BaseModel):
    __tablename__ = "payment"

    user_id = Column(UUID(as_uuid=True), nullable=False)
    order_id = Column(UUID(as_uuid=True), nullable=False)
    payment_id = Column(String(length=128))
    customer_id = Column(String(length=128), nullable=False)
    price_id = Column(String(length=128))
    status = Column(Enum(PaymentState), nullable=False)
    service_name = Column(String(length=128), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
