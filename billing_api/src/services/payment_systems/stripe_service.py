from typing import Optional, Union

import stripe

from core import settings
from db.models import Payment
from schemas.customer import CustomerSchema
from .base import AbstractPaymentSystem
from .schemas import CheckoutInfo, ProviderPayment, ProviderPaymentResult

stripe.api_key = settings.api_key


class StripeService(AbstractPaymentSystem):
    async def create_checkout(
            self,
            payment: Payment,
            success_url: Optional[str] = None,
            cancel_url: Optional[str] = None,
    ) -> Union[CheckoutInfo, str]:

        product_price = ...
        line_items = [
            {
                'price_data': {
                    'currency': payment.product_price_currency,
                    'unit_amount': int(payment.product_price_amount_total * 100),
                    'product_data': {
                        'name': payment.product_name,
                    },
                },
                'quantity': 1,
            },
        ]
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=payment.id,
                line_items=line_items,
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )

            print(f'Checkout URL LINK: {checkout_session.url}')
            return CheckoutInfo(
                checkout_id=checkout_session.stripe_id,
                checkout_url=checkout_session.url,
            )
        except Exception as exc:
            # logger.error(f'Checkout session error: {exc}')
            print(f'Checkout session error: {exc}')
            return str(exc)

    async def create_customer(self) -> CustomerSchema:
        customer = stripe.Customer.create()
        return CustomerSchema(id=customer['id'])

    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        payment_method = await self.customer_payment_method(payment.customer)

        payment_intent = stripe.PaymentIntent.create(
            **payment.dict(),
            payment_method=payment_method,
        )
        return ProviderPaymentResult(
            id=payment_intent['id'],
            client_secret=payment_intent['client_secret'],
        )

    @classmethod
    async def customer_payment_method(cls, customer: str) -> Optional[str]:
        methods = stripe.PaymentMethod.list(
            customer=customer,
            type='card',
        )

        if not methods:
            return None

        return methods['data'][0]['id']


def get_payment_system() -> AbstractPaymentSystem:
    return StripeService()
