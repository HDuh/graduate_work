from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .base_model import BaseModel

__all__ = (
    'User',
)


class User(BaseModel):
    __tablename__ = 'user'

    customer_id = Column(Integer, nullable=False)
    subscription = relationship(
        'Subscription',
        back_populates='user',
    )
    order = relationship(
        'Order',
        back_populates='user',
    )
