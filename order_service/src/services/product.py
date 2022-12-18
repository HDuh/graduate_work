from functools import lru_cache

import stripe
from fastapi import Depends

from src.services import get_db_manager, DbManager
from src.db.models import Product
from src.schemas.product import ProductCreate, ProductList, ProductDetail


class ProductService:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    async def create_product(self, name: str, description: str, price: int,
                             product_type: str = 'Subscription', duration: int = 0,
                             recurring: bool = False, nickname: str = ''):
        recurring_params = None
        if recurring:
            recurring_params = {
                "aggregate_usage": None,
                "interval": "month",
                "interval_count": duration,
                "usage_type": "licensed"
            }

        product_stripe = stripe.Product.create(
            name=name,
            description=description,
        )

        # цена на продукт
        price_stipe = stripe.Price.create(
            currency='rub',
            unit_amount=int(price * 100),
            recurring=recurring_params,
            nickname=nickname,
            product=product_stripe['id']

        )

        product_db = Product(
            name=name,
            product_type=product_type,
            product_stripe_id=product_stripe['id'],
            price_stripe_id=price_stipe['id'],
            description=description,
            duration=duration,
            price=price,
            recurring=recurring,
            currency_code='rub',
        )

        await self.db_manager.add(product_db)

        return ProductCreate(**product_db.to_dict())

    async def get_product(self, product_id: int) -> ProductDetail | None:
        result = await self.db_manager.get_by_id(Product, product_id)
        if result := result.scalars().first():
            return ProductDetail(**result.to_dict())
        return

    async def get_all(self) -> list[ProductList]:

        query = await self.db_manager.get_all(Product)
        result = []

        for row in query:
            result.append(ProductList(**row.to_dict()))

        return result

    async def delete_product(self, product_id) -> dict | None:
        result = await self.db_manager.remove(Product, product_id)

        if result := result.scalars().first():
            stripe.Product.modify(
                result.product_stripe_id,
                active=False
            )
            return {'message': f'Product [{product_id}] was deleted.'}

        return


@lru_cache()
def get_product_service(db_manager: DbManager = Depends(get_db_manager)) -> ProductService:
    return ProductService(db_manager)
