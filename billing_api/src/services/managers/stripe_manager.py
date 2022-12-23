import logging

import stripe
from stripe.api_resources.abstract.createable_api_resource import CreateableAPIResource

from src.core import settings
from src.schemas import OrderSchema

__all__ = (
    'StripeManager',
)

stripe.api_key = settings.stripe_config.secret_key
logger = logging.getLogger(__name__)


class StripeManager:

    @classmethod
    def create_payment_intent(cls, product_instance):
        pay_intent = stripe.PaymentIntent.create(
            amount=product_instance.price * 100,
            currency=product_instance.currency_code,
            payment_method_types=['card'],
        )

        logger.info(f'Payment intent [{pay_intent["id"]}] created.')
        return pay_intent

    @classmethod
    def create_checkout_session(cls, order: OrderSchema) -> CreateableAPIResource:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': order.price_id,
                    'quantity': order.quantity,
                },
            ],
            customer=order.customer_id,
            mode='subscription',
            success_url='http://localhost:8001/api/v1/billing/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8001/api/v1/billing/cancel',
        )
        logger.info(f'Checkout session created.')
        return checkout_session