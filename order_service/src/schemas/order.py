from uuid import UUID

from src.schemas.base import BaseSchema


class OrderCreate(BaseSchema):
    id: UUID
    user_id: UUID
    pay_intent_id: str
