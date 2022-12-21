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
            amount=product_instance.price * 100,
            currency=product_instance.currency_code,
            payment_method_types=['card'],
        )

    @classmethod
    def create_product(cls, name, description):
        return stripe.Product.create(
            name=name,
            description=description,
        )

    @classmethod
    def create_price(cls, price, recurring_params, nickname, product_stripe_id):
        return stripe.Price.create(
            currency='rub',
            unit_amount=int(price * 100),
            recurring=recurring_params,
            nickname=nickname,
            product=product_stripe_id
        )

    @classmethod
    def archive_the_product(cls, product_instance):
        stripe.Product.modify(
            product_instance.product_stripe_id,
            active=False
        )
