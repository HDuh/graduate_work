import stripe
from src.core import settings

__all__ = (
    'StripeManager',
)

stripe.api_key = settings.stripe_config.secret_key


class StripeManager:
    @classmethod
    def create_customer(cls):
        return stripe.Customer.create()

    @classmethod
    def create_payment_intent(cls, product_instance):
        return stripe.PaymentIntent.create(
            amount=product_instance.price,
            currency=product_instance.currency_code,
            payment_method_types=['card'],
        )
