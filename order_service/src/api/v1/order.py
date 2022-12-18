from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.db import get_db_manager
from src.utils.http_bearer_security import security
from src.utils.token_decoder import get_token_payload
from src.core import SubscriptionStatus, OrderStatus, settings
from src.db.models import Order, User, Product
from src.db import StripeManager

router = APIRouter()


# templates = Jinja2Templates(directory="templates")


# @router.get('/')
# def index(request: Request):
#     return templates.TemplateResponse('index.html', {'request': request})


@router.post('/create_order')
async def create_order(product_id=uuid4(),
                       access_token=Depends(security),
                       db_manager=Depends(get_db_manager)):

    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    # user_id = 'fcd1fe3e-364d-4428-b01e-0d5dae477b99'
    if not (user := await db_manager.async_get_info_by_id(User, user_id)):
        customer = StripeManager.create_customer()
        user = User(id=user_id, customer_id=customer['id'])

    if not user.subscription or user.subscription.status == SubscriptionStatus.INACTIVE:
        product = await db_manager.async_get_info_by_id(Product, product_id)
        payment_intent = StripeManager.create_payment_intent(product)
        new_order = Order(
            user_id=user.id,
            pay_intent_id=payment_intent['id'],
            status=OrderStatus.UNPAID
        )
        new_order.append(product) # TODO: отладить
        await db_manager.async_add_object(new_order)
        # TODO: передать заказ в сервис оплаты
    else:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
