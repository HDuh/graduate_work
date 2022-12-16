from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from .transitional_models import order_product_table

__all__ = (
    'Order',
)


class Order(BaseModel):
    __tablename__ = 'order'

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='order')  # many to one
    product = relationship(
        'Product',
        secondary=order_product_table,
        back_populates='order',
        lazy='dynamic'
    )  # связь с продуктами many to many

    def __str__(self):
        return self.name
