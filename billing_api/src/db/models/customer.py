from sqlalchemy import Column, Integer, String

from db.models import BaseModel

__all__ = (
    'Customer',
)


class Customer(BaseModel):
    __tablename__ = 'customer'

    user_id = Column(Integer, unique=True, nullable=False)
    provider_customer_id = Column(String(128))
