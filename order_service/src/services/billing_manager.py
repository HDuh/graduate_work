import aiohttp

from src.core import settings

__all__ = (
    'BillingManager',
)


class BillingManager:

    @classmethod
    async def async_checkout(cls, payload):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    settings.billing_config.checkout_session_url,
                    data=payload.json(),
                    headers={'Content-Type': 'application/json'}
            ) as response:
                return response, await response.json()
