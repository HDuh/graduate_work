from sqlalchemy import Column, String, Integer, Boolean

from db.models import BaseModel

__all__ = (
    'Product',
)


class Product(BaseModel):
    __tablename__ = 'product'
    name = Column(String(128), nullable=False)
    description = Column(String(255))
    period = Column(Integer, nullable=False)  # в месяцах
    price = Column(Integer, nullable=False)
    currency_code = Column(String(3), default='rub')
    recurring = Column(Boolean, default=True)

    def all_columns(self):
        column_names = self.__table__.columns.keys()
        return {column_i: getattr(self, column_i) for column_i in column_names}

    def __str__(self):
        return self.name
