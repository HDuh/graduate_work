from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel

__all__ = (
    'Order',
)


class Order(BaseModel):
    __tablename__ = 'order'
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)  # cвязь one to one
    product_id = ...

    user = relationship(
        'User',
        back_populates='order'
    )  # many to one

    def __str__(self):
        return self.name
