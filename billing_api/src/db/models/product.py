from sqlalchemy import Column, String, Integer, Boolean

from db.models import BaseModel

__all__ = (
    'Product',
)


class Product(BaseModel):
    __tablename__ = 'product'
    name = Column(String(128), nullable=False)
    description = Column(String(255))
    product_stripe_id = Column(String(32))    # id продукта в Stripe
    period = Column(Integer, nullable=False)  # в месяцах
    price = Column(Integer, nullable=False)
    currency_code = Column(String(3), default='rub')
    recurring = Column(Boolean, default=True)

    def __str__(self):
        return self.name
