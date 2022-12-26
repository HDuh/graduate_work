from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core import SubscriptionStatus
from .base_model import BaseModel

__all__ = (
    'Subscription',
)


class Subscription(BaseModel):
    __tablename__ = 'subscription'

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'))  # one to one
    status = Column(Enum(SubscriptionStatus))
    start_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    end_date = Column(DateTime(timezone=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), nullable=False)

    user = relationship("User", back_populates="subscription")
