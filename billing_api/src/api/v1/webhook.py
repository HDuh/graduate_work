import logging

import stripe
from fastapi import APIRouter, Request, Depends

from src.core import WebhookEvents, PaymentState
from src.services.payment_service import PaymentService, get_payment_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    '',
    summary='Event tracking from stripe'
)
async def webhook(
        request: Request,
        payment_service: PaymentService = Depends(get_payment_service)
):
    """
    ## Event tracking from stripe

    And working with them through the webhook service
    """
    json_data = await request.json()
    event = stripe.Event.construct_from(json_data, stripe.api_key)
    message = 'not happened'
    if event.type in (WebhookEvents.PAYMENT_SUCCESS.value, WebhookEvents.PAYMENT_REFUND.value):
        status = (
            PaymentState.PAID
            if event.type == WebhookEvents.PAYMENT_SUCCESS.value
            else PaymentState.CANCELED
        )
        message = await payment_service.async_payment_update(
            status,
            customer_id=event.data.object.customer,
            order_id=event.data.object.metadata.get('order_id'),
        )

    return {'status': message}
