from datetime import datetime
from functools import lru_cache

from fastapi import Depends

from src.core import SubscriptionStatus
from src.services.order import OrderService, get_order_service
from src.services.product import ProductService, get_product_service
from src.services.user import UserService, get_user_service


class WebhookService:
    def __init__(self,
                 order_service: OrderService,
                 product_service: ProductService,
                 user_service: UserService):
        self.order_service = order_service
        self.product_service = product_service
        self.user_service = user_service

    async def update_order(self, event_obj):
        user = await self.user_service.get_by_customer_id(event_obj.customer)

        if event_obj.status == 'succeeded':
            if updated_order := await self.order_service.update_order(user.id, event_obj.stripe_id):
                return f'Order was update: {updated_order.to_dict()}'

    async def subscription_updated(self, event_obj):
        user = await self.user_service.get_by_customer_id(event_obj.customer)

        if not event_obj.canceled_at:
            product = await self.product_service.get_product_by_product_stripe_id(event_obj.plan.product)

            subscription = await self.user_service.create_subscription(
                user_id=user.id,
                start=datetime.utcfromtimestamp(event_obj.current_period_start),
                end=datetime.utcfromtimestamp(event_obj.current_period_end),
                product_id=product.id,
                subscription_id=event_obj.stripe_id,
            )
            return f'Subscription create: {subscription}'

        subscription = await self.user_service.update_subscription(
            user_id=user.id,
            status=SubscriptionStatus.INACTIVE)

        return f'Subscription updated: {subscription}'

    async def subscription_deleted(self, event_obj):
        if user := await self.user_service.get_by_customer_id(event_obj.customer):
            await self.user_service.cancel_subscription(user.id)
            return f'Subscription for user [{user.id}] was canceled'


@lru_cache()
def get_webhook_service(
        order_service: OrderService = Depends(get_order_service),
        product_service: ProductService = Depends(get_product_service),
        user_service: UserService = Depends(get_user_service)
) -> WebhookService:
    return WebhookService(order_service, product_service, user_service)
