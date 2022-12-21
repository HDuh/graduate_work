from dataclasses import dataclass, field
from uuid import UUID

from pydantic import BaseModel

from src.core import ProductTypes

__all__ = (
    'ProductCreateSchema',
    'ProductResponseSchema',
)


@dataclass
class ProductCreateSchema:
    name: str
    product_type: ProductTypes
    description: str
    price: int
    duration: int
    recurring: bool = field(default=True)

    def __post_init__(self):
        self.id: UUID = field(init=False)
        self.recurring_params: dict = field(init=False)
        self.product_stripe_id: str = field(init=False)
        self.price_stripe_id: str = field(init=False)

    def to_dict(self) -> dict:
        return {
            attr: value
            for attr, value in self.__dict__.items()
            if (
                    not attr.startswith('_') and
                    attr not in ('recurring_params', 'id')
            )
        }


class ProductResponseSchema(BaseModel):
    id: UUID
    name: str
    product_type: str
    description: str
    duration: int
    price: int
    currency_code: str
    recurring: bool
    is_active: bool
    product_stripe_id: str
    price_stripe_id: str
