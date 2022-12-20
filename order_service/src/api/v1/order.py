from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from src.services import BillingManager, get_billing_manager
from src.services.order import get_order_service, OrderService

router = APIRouter()


# templates = Jinja2Templates(directory="templates")


@router.post('/create_order',  # Может переименовать в buy product?
             # response_model=OrderCreate,
             status_code=HTTPStatus.CREATED)
async def create_order(product_id=uuid4(),
                       # access_token=Depends(security),
                       order_service: OrderService = Depends(get_order_service),
                       billing_manager: BillingManager = Depends(get_billing_manager)) -> JSONResponse:
    # token_payload = get_token_payload(access_token.credentials)
    # if not (user_id := token_payload.get('user_id')):
    #     raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    user_id = 'fcd1fe3e-364d-4428-b01e-0d5dae477b99'

    result = await order_service.create_order(product_id, user_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)

    response, checkout = await billing_manager.async_checkout(result)
    if response.status == HTTPStatus.OK:
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={'message': checkout['url']}
        )

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={'message': 'checkout session error'}
    )
