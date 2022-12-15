import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, Date

from db.models import BaseModel


class SubscriptionState(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELED = "canceled"


class Subscription(BaseModel):
    user_id = Column(Integer)
    product_id = Column(ForeignKey('product.id'))
    state = Column(Enum(SubscriptionState))
    start_date = Column(Date)
    end_date = Column(Date)
