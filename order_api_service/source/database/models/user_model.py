from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base_model import BaseModel

__all__ = (
    'User',
)


class User(BaseModel):
    __tablename__ = 'user'

    customer_id = Column(UUID(as_uuid=True), nullable=False)
    subscription = relationship(
        'Subscription',
        back_populates='user',
    )
    order = relationship(
        'Order',
        back_populates='user',
    )
