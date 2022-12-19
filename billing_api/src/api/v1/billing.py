from typing import Any

import stripe
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.core import settings
from src.schemas.order import OrderSchema

# from fastapi.responses import JSONResponse

stripe.api_key = settings.stripe_config.secret_key
router = APIRouter()
DOMAIN = 'localhost:8001'

templates = Jinja2Templates(directory="templates")


@router.get('/ping', summary='Ping func')
async def ping_func() -> dict:
    return {'status': 'ok'}


@router.get('/success')
async def success(request: Request):
    return templates.TemplateResponse('success.html', {'request': request})


@router.get('/cancel')
async def cancel(request: Request):
    return templates.TemplateResponse('cancel.html', {'request': request})


@router.post('/create_checkout_session')
async def create_checkout_session(
        order_schema: OrderSchema
) -> Any:
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': order_schema.price_id,
                    'quantity': order_schema.quantity,
                },
            ],
            customer=order_schema.customer_id,
            mode='subscription',
            success_url='http://localhost:8001/api/v1/billing/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8001/api/v1/billing/cancel',
        )

        print(checkout_session)
    except Exception as e:
        return str(e)

    return checkout_session
