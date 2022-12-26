import datetime
from uuid import UUID

from src.schemas.base import BaseMixin


class DeactivateSubscription(BaseMixin):
    user_id: UUID


class DeactivateComplete(BaseMixin):
    user_id: UUID
    end_date: datetime.datetime
    product_id: UUID
    status: str


class Create(BaseMixin):
    user_id: UUID
    start_date: datetime.datetime
    end_date: datetime.datetime
    product_id: UUID
