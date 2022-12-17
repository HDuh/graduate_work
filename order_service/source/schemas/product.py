from source.schemas.base import BaseSchema


class ProductCreate(BaseSchema):
    name: str
    description: str
    price: int
    period: int
    recurring: bool


class ProductList(BaseSchema):
    id: int
    name: str
    price: int
    currency_code: str
    period: int


class ProductDetail(BaseSchema):
    id: int
    name: str
    description: str
    period: int
    price: int
    currency_code: str
    recurring: bool
