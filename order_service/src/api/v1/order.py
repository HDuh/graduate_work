from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.db import get_db_manager
from src.utils.http_bearer_security import security
from src.utils.token_decoder import get_token_payload
from src.core import SubscriptionStatus, OrderStatus
from src.db.models import Order, User, Product

router = APIRouter()

# templates = Jinja2Templates(directory="templates")


# @router.get('/')
# def index(request: Request):
#     return templates.TemplateResponse('index.html', {'request': request})


@router.post('/create_order')
async def create_order(product_id,
                       access_token=Depends(security),
                       db_manager=Depends(get_db_manager)):
    '''распаковать токен. проверить есть ли юзер у нас в бд. если есть, проверить есть ли активная подписка.
    если нет создать кастомер id, добавить юзера в БД.'''
    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    # user_id = 'fcd1fe3e-364d-4428-b01e-0d5dae477b99'
    if user := await db_manager.async_get_info_by_id(User, user_id):
        if user.subscription and user.subscription.status == SubscriptionStatus.INACTIVE:
            new_order = Order(
                user_id=user.id,
                pay_intent_id='random_id',
                status=OrderStatus.UNPAID
            )
            product = db_manager.async_get_info_by_id(Product, product_id)
            new_order.append(product)
            await db_manager.async_add_object(new_order)
            # TODO: передать заказ в сервис оплаты
        # else:
        #     raise HTTPException(status_code=HTTPStatus.CONFLICT)

    # TODO: получить castomer_id. Можно через ручку?! или добавить менеджера для работы с страйп


