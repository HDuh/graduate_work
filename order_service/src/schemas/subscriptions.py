import datetime
from uuid import UUID

from src.schemas.base import BaseSchema


class DeactivateSubscription(BaseSchema):
    user_id: UUID


class Deactivate(BaseSchema):
    user_id: UUID
    end_date: datetime.datetime
    product_id: UUID
    status: str


class SubscriptionCreate(BaseSchema):
    user_id: UUID
    start_date: datetime.datetime
    end_date: datetime.datetime
    product_id: UUID


class ProductSchema(BaseSchema):
    id: str
    name: str
    price: int


class SubscriptionSchema(BaseSchema):
    user_id: str
    product_id: str
