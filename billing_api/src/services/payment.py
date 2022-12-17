from functools import lru_cache

from db.models import Customer
from db.models import Payment, PaymentState
from fastapi import Depends
from services.customer import CustomerService, get_customer_service
from services.payment_systems.schemas import ProviderPayment, ProviderPaymentCancel, ProviderPaymentResult
from services.subscriptions import SubscriptionService, get_subscriptions_service
from sqlalchemy import desc, select, update
from sqlalchemy.orm import Session

from schemas.payment import (
    AddPaymentSchema, NewPaymentSchema, PaymentCancel, PaymentSchema, UpdatePaymentSchema,
)
from schemas.subscriptions import SubscriptionSchema


class PaymentAuthenticatedService(object):

    def __init__(
            self,
            db: Session,
            user_id: str,
            provider: AbstractProvider,
            subscriptions: SubscriptionService,
            customers: CustomerService,
    ):
        self.db = db
        self.user_id = user_id
        self.provider = provider
        self.subscriptions = subscriptions
        self.customers = customers

    async def new_payment(self, payment: NewPaymentSchema) -> ProviderPaymentResult:
        customer = await self.customers.get_customer(self.user_id)
        product = await self.subscriptions.get_product(payment.product)

        provider_payment = ProviderPayment(
            amount=product.price,
            currency=payment.currency,
            customer=customer.provider_customer_id,
        )
        invoice = await self.provider.create_payment(provider_payment)

        payment_db = Payment(
            customer_id=customer.id,
            invoice_id=invoice.id,
            product_id=product.id,
            status=PaymentState.PROCESSING,
        )
        self.db.add(payment_db)

        return invoice


class PaymentService(object):

    def __init__(
            self,
            db: Session,
            provider: AbstractProvider,
            subscriptions: SubscriptionService,
            customers: CustomerService,
    ):
        self.db = db
        self.provider = provider
        self.subscriptions = subscriptions
        self.customers = customers

    async def get_payment(self, invoice_id: str) -> Payment:
        payment = await self.db.execute(
            select(
                Payment.id,
                Payment.status,
                Payment.product_id,
                Customer.user_id,
            ).outerjoin(
                Customer, Payment.customer_id == Customer.id,
            ).where(
                Payment.invoice_id == invoice_id,
            ),
        )
        if not payment:
            raise PaymentNotFound

        return payment.first()

    async def get_last_payment(self, customer_id: int) -> Payment:
        payment = await self.db.execute(
            select(
                Payment.id,
                Payment.invoice_id,
            ).where(
                Payment.customer_id == customer_id,
            ).order_by(desc(Payment.id)),
        )
        if not payment:
            raise PaymentNotFound

        return payment.first()

    async def add_payment(self, payment: AddPaymentSchema):
        customer = await self.customers.get_customer(payment.user_id)

        payment_db = Payment(
            customer_id=customer.id,
            product_id=payment.product_id,
            status=PaymentState.PRE_PROCESSING,
        )
        self.db.add(payment_db)
        await self.db.flush()

        provider_payment = ProviderPayment(
            amount=payment.amount,
            currency=payment.currency,
            customer=customer.provider_customer_id,
            confirm=True,
        )
        invoice = await self.provider.create_payment(provider_payment)

        payment_db.invoice_id = invoice.id
        payment_db.status = PaymentState.PROCESSING
        self.db.add(payment_db)

    async def get_processing(self) -> list[PaymentSchema]:
        processing_payments = await self.db.execute(
            select(
                Payment.id,
                Payment.invoice_id,
                Payment.product_id,
                Payment.status,
                Customer.user_id,
            ).outerjoin(
                Customer, Payment.customer_id == Customer.id,
            ).where(
                Payment.status == PaymentState.PROCESSING,
            ),
        )
        return processing_payments.all()

    async def update_status(self, payment: UpdatePaymentSchema):
        await self.db.execute(
            update(
                Payment,
            ).where(
                Payment.invoice_id == payment.invoice_id,
            ).values(
                status=payment.status,
            ),
        )
        await self.db.flush()
        payment_db = await self.get_payment(payment.invoice_id)

        if payment.status == PaymentState.PAID:
            subscription = SubscriptionSchema(
                user_id=payment_db.user_id,
                product_id=payment_db.product_id,
            )
            await self.subscriptions.update_subscription(subscription)

    async def cancel(self, cancel_info: PaymentCancel):

        customer = await self.customers.get_customer(cancel_info.user_id)
        payment = await self.get_last_payment(customer.id)

        provider_cancel = ProviderPaymentCancel(
            amount=cancel_info.amount,
            currency=cancel_info.currency,
            customer=customer.provider_customer_id,
            payment=payment.invoice_id,
        )
        await self.provider.cancel(provider_cancel)

        update_payment = UpdatePaymentSchema(
            invoice_id=payment.invoice_id,
            status=PaymentState.CANCELED,
        )
        await self.update_status(update_payment)


@lru_cache(maxsize=128)
def get_payment_auth_service(
        db: Session = Depends(get_db),
        user_id: str = Depends(get_auth),
        provider: AbstractProvider = Depends(get_default_provider),
        subscriptions: SubscriptionService = Depends(get_subscriptions_service),
        customers: CustomerService = Depends(get_customer_service),
):
    return PaymentAuthenticatedService(
        db=db,
        user_id=user_id,
        provider=provider,
        subscriptions=subscriptions,
        customers=customers,
    )


@lru_cache(maxsize=128)
def get_payment_service(
        db: Session = Depends(get_db),
        provider: AbstractProvider = Depends(get_default_provider),
        subscriptions: SubscriptionService = Depends(get_subscriptions_service),
        customers: CustomerService = Depends(get_customer_service),
):
    return PaymentService(
        db=db,
        provider=provider,
        subscriptions=subscriptions,
        customers=customers,
    )
