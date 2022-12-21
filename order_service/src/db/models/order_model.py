import datetime

from sqlalchemy import Column, ForeignKey, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core import OrderStatus
from .base_model import BaseModel
from .transitional_models import order_product_table

__all__ = (
    'Order',
)


class Order(BaseModel):
    __tablename__ = 'order'

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='order')  # many to one
    # product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), nullable=False)
    product = relationship(
        'Product',
        secondary=order_product_table,
        back_populates='order',
        lazy='selectin'
    )  # связь с продуктами many to many
    status = Column(Enum(OrderStatus))
    pay_intent_id = Column(String(128))
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

    def __str__(self):
        return self.name
