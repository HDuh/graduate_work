import logging

import stripe

from src.core import settings

__all__ = (
    'StripeManager',
)

stripe.api_key = settings.stripe_config.secret_key
logger = logging.getLogger(__name__)


class StripeManager:
    @classmethod
    def create_customer(cls):
        customer = stripe.Customer.create()

        logger.info(f'Customer [{customer["id"]}] created.')
        return customer

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
    def create_product(cls, name, description):
        product = stripe.Product.create(
            name=name,
            description=description,
        )

        logger.info(f'Product [{product["id"]}] created.')
        return product

    @classmethod
    def create_price(cls, price, recurring_params, nickname, product_stripe_id):
        price = stripe.Price.create(
            currency='rub',
            unit_amount=int(price * 100),
            recurring=recurring_params,
            nickname=nickname,
            product=product_stripe_id
        )

        return price

    @classmethod
    def archive_the_product(cls, product_instance):
        product = stripe.Product.modify(
            product_instance.product_stripe_id,
            active=False
        )
        logger.info(f'Product [{product["id"]}] archived.')
        return product

    @classmethod
    def add_to_metadata(cls, subscription_id, user_id, order_id):
        result = stripe.Subscription.modify(
            subscription_id,
            metadata={
                "user_id": user_id,
                "order_id": order_id,
            },
        )
        logger.info(f'User id [{user_id}] added to subscription [{subscription_id}] .')
        logger.info(f'Order id [{order_id}] added to subscription [{subscription_id}] .')
        return result

    @classmethod
    def cancel_subscription(cls, user_id):
        subscription_query = stripe.Subscription.search(
            query=f"status:'active' AND metadata['user_id']:'{user_id}'",
        )
        subscription_obj = subscription_query['data'][0]
        subscription_id = subscription_obj['id']

        result = stripe.Subscription.delete(
            subscription_id,
        )
        logger.info(f'Subscription cancelled for user [{user_id}].')
        return result

    @classmethod
    def deactivate_subscription(cls, user_id):
        subscription_query = stripe.Subscription.search(
            query=f"status:'active' AND metadata['user_id']:'{user_id}'",
        )
        if subscription_query:
            subscription_obj = subscription_query['data'][0]
            subscription_id = subscription_obj['id']

            result = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True)

            logger.info(f'Subscription deactivated for user [{user_id}].')
            return result

    @classmethod
    def refund(cls, amount, pay_intent_id, order_id):
        refund = stripe.Refund.create(
            amount=amount * 100,
            payment_intent=pay_intent_id,
            metadata={
                'order_id': order_id,
            }
        )
        logger.info(f'Refund for payment intent [{pay_intent_id}].')
        return refund
