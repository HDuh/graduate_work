from source.schemas.base import BaseSchema


class ProductSchema(BaseSchema):
    id: str
    name: str
    price: int


class SubscriptionSchema(BaseSchema):
    user_id: str
    product_id: str
