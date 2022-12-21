from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID

from src.core import ActivationChoice
from .base_model import BaseModel

__all__ = (
    'Subscription',
)


class Subscription(BaseModel):
    __tablename__ = 'subscription'

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'))  # one to one
    status = Column(Enum(ActivationChoice))
    start_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    end_date = Column(DateTime(timezone=True), nullable=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), nullable=False)

    # user = relationship("User", lazy='selectin')

    def __str__(self):
        return self.name
