from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from stripe.api_resources.abstract.createable_api_resource import CreateableAPIResource

from src.schemas import PaymentFullSchema, PaymentShortSchema
from src.schemas.order_schema import OrderSchema
from src.services.managers import StripeManager
from src.services.payment_service import get_payment_service, PaymentService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/success')
async def success(request: Request):
    return templates.TemplateResponse('success.html', {'request': request})


@router.get('/cancel')
async def cancel(request: Request):
    return templates.TemplateResponse('cancel.html', {'request': request})


@router.post('/checkout')
async def create_checkout_session(
        order_schema: OrderSchema,
        payment_service: PaymentService = Depends(get_payment_service)
) -> CreateableAPIResource:
    """
        ## Create checkout session

        Create checkout session, save info to DB and return checkout session to _order_service_.

        Gets order model from _order_service_, create __check out session__ and return it.
    """

    checkout_session = StripeManager.create_checkout_session(order_schema)
    await payment_service.async_build_and_create(order_schema)
    return checkout_session


@router.get(
    '/',
    summary='Get list of payments',
    response_model=list[PaymentShortSchema],
    status_code=HTTPStatus.OK
)
async def get_all_payment_info(
        payment_service: PaymentService = Depends(get_payment_service)
) -> list[PaymentShortSchema]:
    """
        ## Get list of products with the information below:
        _id_
        _user_id_
        _order_id_
        _status_
        _service_name_
        _created_at_
    """
    all_payments = await payment_service.get_all()
    return [PaymentShortSchema(**payment.__dict__) for payment in all_payments]


@router.get(
    '/{user_id}',
    summary='',
    response_model=PaymentFullSchema,
    status_code=HTTPStatus.OK
)
async def full_info_by_user(
        user_id: UUID,
        payment_service: PaymentService = Depends(get_payment_service)
) -> PaymentFullSchema:
    """
        ## Get detailed information about payment by user ID the information below:
        _id_
        _user_id_
        _order_id_
        _payment_id_
        _customer_id_
        _price_id_
        _status_
        _service_name_
        _created_at_
        _updated_at_

        URL params:
        - **{user_id}**
    """
    if not (payment := await payment_service.get_by_id(user_id=user_id)):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User {user_id} not found'
        )
    return PaymentFullSchema(**payment.__dict__)


@router.get(
    '/{order_id}',
    summary='',
    response_model=PaymentFullSchema,
    status_code=HTTPStatus.OK
)
async def full_info_by_order(
        order_id: UUID,
        payment_service: PaymentService = Depends(get_payment_service)
) -> PaymentFullSchema:
    """
        ## Get detailed information about payment by order ID the information below:
        _id_
        _user_id_
        _order_id_
        _payment_id_
        _customer_id_
        _price_id_
        _status_
        _service_name_
        _created_at_
        _updated_at_

        URL params:
        - **{order_id}**
    """
    if not (payment := await payment_service.get_by_id(order_id=order_id)):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Order {order_id} not found'
        )
    return PaymentFullSchema(**payment.__dict__)
