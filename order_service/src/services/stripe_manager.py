import stripe

from src.core import settings

__all__ = (
    'StripeManager',
)

stripe.api_key = settings.stripe_config.secret_key


class StripeManager:

    @classmethod
    def create_customer(cls):
        """
        Создать customer в stripe
        """
        return stripe.Customer.create()

    # @classmethod
    # def create_payment_intent(cls, product_instance):
    #     return stripe.PaymentIntent.create(
    #         amount=product_instance.price * 100,
    #         currency=product_instance.currency_code,
    #         payment_method_types=['card'],
    #     )

    @classmethod
    def create_product(cls, product_instance):
        """
        Создать продукт в stripe
        """
        return stripe.Product.create(
            name=product_instance.name,
            description=product_instance.description,
        )

    @classmethod
    def create_price(cls, product_instance):
        """
        Создать price в stripe
        """
        return stripe.Price.create(
            currency='rub',
            unit_amount=product_instance.price * 100,
            recurring=product_instance.recurring_params,
            product=product_instance.product_stripe_id
        )

    @classmethod
    def archive_product(cls, product_instance, status=False):
        """
        Изменить статус продукта в stripe
        """
        stripe.Product.modify(
            product_instance.product_stripe_id,
            active=status
        )
