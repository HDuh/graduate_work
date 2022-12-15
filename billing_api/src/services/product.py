from functools import lru_cache

import stripe
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from db.models import Product
from schemas.product import ProductCreate, ProductList, ProductDetail


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, name: str, description: str, price: int,
                             period: int = 0, recurring: bool = False,
                             nickname: str = ''):
        recurring_params = None
        if recurring:
            recurring_params = {
                "aggregate_usage": None,
                "interval": "month",
                "interval_count": period,
                "usage_type": "licensed"
            }

        product_stripe = stripe.Product.create(
            name=name,
            description=description,
        )

        # цена на продукт
        stripe.Price.create(
            currency='rub',
            unit_amount=int(price * 100),
            recurring=recurring_params,
            nickname=nickname,
            product=product_stripe['id']

        )

        product_db = Product(
            name=name,
            description=description,
            period=period,
            price=price,
            recurring=recurring,
            currency_code='rub',
            product_stripe_id=product_stripe['id']
        )

        self.session.add(product_db)
        return ProductCreate(**product_db.to_dict())

    async def get_product(self, product_id: int) -> ProductDetail | None:
        result = await self.session.execute(
            select(Product)
            .where(Product.id == product_id)
        )

        if result := result.scalars().first():
            return ProductDetail(**result.to_dict())
        return None

    async def get_all(self) -> list[ProductList]:
        query = await self.session.execute(
            select(Product)
            .order_by(
                Product.id
            )
        )
        query = query.scalars().all()
        result = []

        for row in query:
            result.append(ProductList(**row.to_dict()))

        return result

    async def delete_product(self, product_id) -> dict | None:
        result = await self.session.execute(
            select(Product)
            .where(Product.id == product_id)
        )

        if result := result.scalars().first():
            stripe.Product.modify(
                result.product_stripe_id,
                active=False
            )
            await self.session.delete(result)
            return {product_id: 'deleted'}

        return None


@lru_cache()
def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(session)
