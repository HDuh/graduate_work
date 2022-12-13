from sqlalchemy import Column, String, Integer

from db.models import BaseModel

__all__ = (
    'Product',
)


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(128), nullable=False)
    description = Column(String(128))
    price = Column(Integer())
    currency_code = Column(String(3), default='RUB')

    def __str__(self):
        return self.name
