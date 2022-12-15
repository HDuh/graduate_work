from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from .base_model import BaseModel

__all__ = (
    'Subscription',
)


class Subscription(BaseModel):
    __tablename__ = 'subscription'
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)  # cвязь one to one
    status = Column(String(32), nullable=False)
    start_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    end_date = Column(DateTime(timezone=True), nullable=False)

    product_id = Column(Integer, ForeignKey('product.id'), ondelete='CASCADE', nullable=False)

    def __str__(self):
        return self.name
