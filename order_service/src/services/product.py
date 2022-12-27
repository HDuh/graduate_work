import logging
from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_session
from src.db.models import Product
from src.services.managers.stripe_manager import StripeManager
from .base_db_service import BaseDBService

logger = logging.getLogger(__name__)


class ProductService(BaseDBService):

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

        product_stripe = StripeManager.create_product(name, description)

        # цена на продукт
        price_stipe = StripeManager.create_price(
            price=price,
            recurring_params=recurring_params,
            nickname=nickname,
            product_stripe_id=product_stripe.stripe_id)

        product_db = Product(
            name=name,
            product_type=product_type,
            product_stripe_id=product_stripe.stripe_id,
            price_stripe_id=price_stipe.stripe_id,
            description=description,
            duration=duration,
            price=price,
            recurring=recurring,
            currency_code='rub',
        )

        await self.add(product_db)
        logger.info(f'Product [%s] added to DB.', product_db.id)
        return product_db

    async def delete_product(self, product_id):
        result = await self.remove(product_id)
        logger.info(f'Product [%s] removed from DB.', product_id)
        StripeManager.archive_the_product(result)

    async def get_product_by_product_stripe_id(self, product_stripe_id):
        result = await self.session.execute(
            select(Product)
            .where(Product.product_stripe_id == product_stripe_id)
        )
        return result.scalar()


@lru_cache()
def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(session, Product)
