from uuid import UUID

from .base_schema_mixin import BaseMixin


class ProductCreate(BaseMixin):
    name: str
    product_type: str
    description: str
    price: int
    duration: int
    recurring: bool


class ProductList(BaseMixin):
    id: UUID
    name: str
    price: int
    currency_code: str
    duration: int


class ProductDetail(BaseMixin):
    id: UUID
    name: str
    description: str
    duration: int
    price: int
    currency_code: str
    recurring: bool
