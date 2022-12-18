from uuid import UUID

from src.schemas.base import BaseSchema


class ProductCreate(BaseSchema):
    name: str
    product_type: str
    description: str
    price: int
    duration: int
    recurring: bool


class ProductList(BaseSchema):
    id: UUID
    name: str
    price: int
    currency_code: str
    duration: int


class ProductDetail(BaseSchema):
    id: UUID
    name: str
    description: str
    duration: int
    price: int
    currency_code: str
    recurring: bool
