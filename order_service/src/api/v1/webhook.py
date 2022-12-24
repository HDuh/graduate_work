import logging

import stripe
from fastapi import APIRouter, Request, Depends

from src.services.webhook import WebhookService, get_webhook_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    '',
    summary='Event tracking from stripe'
)
async def webhook(
        request: Request,
        webhook_service: WebhookService = Depends(get_webhook_service)
):
    """
    ## Event tracking from stripe

    And working with them through the webhook service
    """
    json_data = await request.json()
    event = stripe.Event.construct_from(json_data, stripe.api_key)
    event_type = event['type']
    message = 'not happened'

    if event_type == 'payment_intent.succeeded':
        logger.info(event_type)
        payment_intent_obj = event['data']['object']
        message = await webhook_service.update_order(payment_intent_obj)

    elif event_type == 'customer.subscription.updated':
        logger.info(event_type)
        subscription_event = event['data']['object']
        message = await webhook_service.subscription_updated(subscription_event)

    if event_type == 'customer.subscription.deleted':
        logger.info(event_type)
        subscription_event = event['data']['object']
        message = await webhook_service.subscription_deleted(subscription_event)

    else:
        logger.info('ANOTHER TYPE')
        logger.info(event.type)

    return {'status': message}
