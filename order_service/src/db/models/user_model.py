from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel

__all__ = (
    'User',
)


class User(BaseModel):
    __tablename__ = 'user'

    customer_id = Column(String(128), nullable=False)
    subscription = relationship(
        'Subscription',
        back_populates='user',
        lazy='subquery'
    )
    order = relationship(
        'Order',
        back_populates='user',
        lazy='subquery'
    )
