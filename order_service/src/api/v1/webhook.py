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

    if event.type == 'payment_intent.succeeded':
        logger.info(event.type)
        message = await webhook_service.update_order(event.data.object)
        logger.info(message)

    elif event.type == 'customer.subscription.updated':
        logger.info(event.type)
        message = await webhook_service.subscription_updated(event.data.object)
        logger.info(message)

    if event.type == 'customer.subscription.deleted':
        logger.info(event.type)
        message = await webhook_service.subscription_deleted(event.data.object)
        logger.info(message)

    else:
        logger.info('ANOTHER TYPE -> %s', event.type)
