import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

from src.schemas.order import OrderForBilling
from src.services import BillingManager, get_billing_manager
from src.services.order import get_order_service, OrderService
from src.utils.token_decoder import get_token_payload

router = APIRouter()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="/app/src/templates")


@router.get('')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/home')
def index(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.post('',
             summary='Create order',
             status_code=HTTPStatus.CREATED)
async def create_order(order_schema: OrderForBilling,
                       order_service: OrderService = Depends(get_order_service),
                       billing_manager: BillingManager = Depends(get_billing_manager)) -> JSONResponse:
    """
        ## Create Order

        Save Order instance to DB with status [Unpaid] and send info to _billing_api_.

        Gets __url link__ from _billing_api_ to create __check out session__ and return it.
    """
    token_payload = get_token_payload()
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    product_id = order_schema.product_id
    result = await order_service.create_order(product_id, user_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)

    response, checkout = await billing_manager.async_checkout(result)

    if response.status == HTTPStatus.OK:
        logger.info(f"Order for user [%s] created successfully! URL %s", user_id, checkout['url'])
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content={"sessionId": checkout['id'], "checkoutUrl": checkout['url']}
        )

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={'message': 'checkout session error'}
    )
