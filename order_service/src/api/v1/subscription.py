from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse
from stripe.error import InvalidRequestError

from src.schemas.order import OrderRefundCreate, OrderRefundComplete
from src.schemas.subscriptions import DeactivateSubscription, Deactivate
from src.services.order import get_order_service, OrderService
from src.services.user import get_user_service, UserService

router = APIRouter()


@router.post('/refund',
             status_code=HTTPStatus.OK)
async def refund(
        refund_schema: OrderRefundCreate,
        order_service: OrderService = Depends(get_order_service)) -> OrderRefundComplete | JSONResponse:
    """ Возврат денежных средств и отмена подписки """
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


@router.post('/deactivate',
             status_code=HTTPStatus.OK)
async def deactivate_subscription(
        subscription_schema: DeactivateSubscription,
        user_service: UserService = Depends(get_user_service)) -> Deactivate | JSONResponse:
    """ Приостановление подписки без продления оплаты """
    result = await user_service.deactivate_subscription(**subscription_schema.dict())

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return Deactivate(**result.to_dict())
