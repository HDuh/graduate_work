from sqlalchemy import Column, String, Integer, Boolean, Float
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from .transitional_models import order_product_table

__all__ = (
    'Product',
)


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(128), nullable=False)
    product_type = Column(String(128), nullable=False)  # или ENUM
    product_stripe_id = Column(String(32))  # id продукта в Stripe
    description = Column(String(255))
    duration = Column(Integer, nullable=False)  # в месяцах
    price = Column(Float, nullable=False)
    currency_code = Column(String(3), default='rub')
    recurring = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    subscription = relationship()  # связь one to many
    order = relationship(
        'Order',
        secondary=order_product_table,
        back_populates='product',
        lazy='dynamic',
        passive_deletes=True,
    )  # связь с заказами many to many

    def __str__(self):
        return self.name
