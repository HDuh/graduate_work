import aiohttp
from src.schemas.subscriptions import ProductSchema, SubscriptionSchema

from src.core.config import SubscriptionsSettings, settings


class SubscriptionService(object):
    settings: SubscriptionsSettings = settings.subscriptions

    @classmethod
    async def get_product(cls, product_id: str) -> ProductSchema:
        session = aiohttp.ClientSession()
        async with session.get(f'{cls.settings.url}/product/{product_id}') as response:
            body = await response.json()
            product = ProductSchema(**body)
        await session.close()
        return product

    @classmethod
    async def update_subscription(cls, subscription: SubscriptionSchema) -> None:
        session = aiohttp.ClientSession()
        url = f'{cls.settings.url}/service/subscription'
        body = subscription.dict()

        response = await session.post(url, json=body) # noqa
        await session.close()


def get_subscriptions_service():
    return SubscriptionService()