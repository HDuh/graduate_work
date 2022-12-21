import datetime
from uuid import UUID

from src.schemas.base import BaseSchema


class DeactivateSubscription(BaseSchema):
    user_id: UUID


class DeactivateComplete(BaseSchema):
    user_id: UUID
    end_date: datetime.datetime
    product_id: UUID
    status: str


class Create(BaseSchema):
    user_id: UUID
    start_date: datetime.datetime
    end_date: datetime.datetime
    product_id: UUID
