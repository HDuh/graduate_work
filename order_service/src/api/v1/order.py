from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse
from stripe.error import InvalidRequestError

from src.schemas.order import OrderRefundCreate, OrderRefundComplete
from src.schemas.subscriptions import DeactivateSubscription, Deactivate
from src.services import BillingManager, get_billing_manager
from src.services.order import get_order_service, OrderService
from src.services.user import get_user_service, UserService

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

    user_id = 'b20da6d8-9178-4622-8e6a-30572cbaacd4'

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


@router.post('/refund',
             status_code=HTTPStatus.OK)
async def refund(
        refund_schema: OrderRefundCreate,
        order_service: OrderService = Depends(get_order_service)) -> OrderRefundComplete | JSONResponse:
    try:
        result = await order_service.create_refund(**refund_schema.dict())

        if not result:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

        return OrderRefundComplete(**result)

    except InvalidRequestError as _ex:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={
                'message': f'User [{refund_schema.user_id}] '
                           f'already refund money for product [{refund_schema.product_id}]'}
        )


@router.post('/deactivate_subscription',
             status_code=HTTPStatus.OK)
async def deactivate_subscription(
        subscription_schema: DeactivateSubscription,
        user_service: UserService = Depends(get_user_service)) -> Deactivate | JSONResponse:
    result = await user_service.deactivate_subscription(**subscription_schema.dict())

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return Deactivate(**result.to_dict())
