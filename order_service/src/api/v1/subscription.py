import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse
from stripe.error import InvalidRequestError

from src.schemas.order import RefundCreate, RefundComplete
from src.schemas.subscriptions import DeactivateSubscription, DeactivateComplete
from src.services.order import get_order_service, OrderService
from src.services.user import get_user_service, UserService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/refund',
             summary='Refund and cancel subscription',
             status_code=HTTPStatus.OK)
async def refund(
        refund_schema: RefundCreate,
        order_service: OrderService = Depends(get_order_service)) -> RefundComplete | JSONResponse:
    """
        ## Refund money and cancel subscription.

        Send refund info to stripe.

        If success:

            DB changes:
             - __user subscription status__:  _[Canceled]_
             - __user order status__:  _[Canceled]_

        Else:

            Please try again latter :)

     """
    try:
        logger.info(f'User [ {refund_schema.user_id} ] trying refund money for product [ {refund_schema.product_id} ]')
        result = await order_service.create_refund(**refund_schema.dict())

        if not result:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        logger.info(f'User [ {refund_schema.user_id} ] SUCCESSFULLY refund money for product [ {refund_schema.product_id} ]')
        return RefundComplete(**result)

    except InvalidRequestError as _ex:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={
                'message': f'User [{refund_schema.user_id}] '
                           f'already refund money for product [{refund_schema.product_id}]'}
        )


@router.post('/deactivate',
             summary='Suspension of subscription without refund',
             status_code=HTTPStatus.OK)
async def deactivate_subscription(
        subscription_schema: DeactivateSubscription,
        user_service: UserService = Depends(get_user_service)) -> DeactivateComplete | JSONResponse:
    """
        ## Suspension of subscription without refund.

        The subscription is cancelled at the end of the period.
        Send user subscription update info to stripe.

        If success:

            DB changes:
             - __user subscription status__:  _[Inactive]_

        Else:
        
            Please try again latter :)

     """

    result = await user_service.deactivate_subscription(**subscription_schema.dict())

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    logger.info(f'User [ {subscription_schema.user_id} ] deactivate subscription.')

    return DeactivateComplete(**result.to_dict())
