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
        return stripe.Product.modify(
            product_instance.product_stripe_id,
            active=False
        )

    @classmethod
    def add_user_id_to_subscription(cls, subscription_id, user_id):
        return stripe.Subscription.modify(
            subscription_id,
            metadata={"user_id": user_id},
        )

    @classmethod
    def cancel_subscription(cls, user_id):
        subscription_query = stripe.Subscription.search(
            query=f"status:'active' AND metadata['user_id']:'{user_id}'",
        )
        print(subscription_query)
        subscription_obj = subscription_query['data'][0]

        subscription_id = subscription_obj['id']

        return stripe.Subscription.delete(
            subscription_id,
        )

    @classmethod
    def deactivate_subscription(cls, user_id):
        subscription_query = stripe.Subscription.search(
            query=f"status:'active' AND metadata['user_id']:'{user_id}'",
        )
        if subscription_query:
            subscription_obj = subscription_query['data'][0]
            subscription_id = subscription_obj['id']

            return stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True)

    @classmethod
    def refund(cls, amount, pay_intent_id):
        return stripe.Refund.create(
            amount=amount * 100,
            payment_intent=pay_intent_id,
        )
