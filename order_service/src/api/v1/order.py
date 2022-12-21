from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from src.services import BillingManager, get_billing_manager
from src.services.order import get_order_service, OrderService

router = APIRouter()


@router.post('',
             status_code=HTTPStatus.CREATED)
async def create_order(product_id=uuid4(),
                       # access_token=Depends(security),
                       order_service: OrderService = Depends(get_order_service),
                       billing_manager: BillingManager = Depends(get_billing_manager)) -> JSONResponse:
    """ Создание заказа и отправка информации в billing_api, колбэком получаем ссылку на оплату """
    # token_payload = get_token_payload(access_token.credentials)
    # if not (user_id := token_payload.get('user_id')):
    #     raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    user_id = 'b20da6d8-9178-4622-8e6a-30572cbaacd4'

    result = await order_service.create_order(product_id, user_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)

    response, checkout = await billing_manager.async_checkout(result)
    if response.status == HTTPStatus.CREATED:
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={'message': checkout['url']}
        )

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={'message': 'checkout session error'}
    )
