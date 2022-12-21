from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref

from .base_model import BaseModel

__all__ = (
    'User',
)


class User(BaseModel):
    __tablename__ = 'user'

    customer_id = Column(String(128), nullable=False)
    subscription = relationship(
        'Subscription',
        backref='user',
        uselist=False,
        lazy='selectin'
    )
    order = relationship(
        'Order',
        back_populates='user',
        lazy='selectin'
    )
