from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.core import SubscriptionStatus
from src.db.models import Product
from src.services import DbManager, BillingManager
from src.services.order_manager import OrderManager

router = APIRouter()


@router.post('/buy_product')
async def buy_product(product_id: UUID,
                      # access_token=Depends(security),
                      ) -> JSONResponse:
    # token_payload = get_token_payload(access_token.credentials)
    # if not (user_id := token_payload.get('user_id')):
    #     raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    user_id = 'fcd1fe3e-364d-4428-b01e-0d5dae477b98'

    user = await DbManager.async_check_or_create_user(user_id)

    user_subscription = await DbManager.async_get_user_subscription(user.id)
    if user_subscription and user_subscription.status == SubscriptionStatus.ACTIVE:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'message': f'user {user_id} already has an active subscription'}
        )

    product = await DbManager.async_get_by_id(Product, product_id)
    order = await OrderManager.async_build_and_create(user, product)

    response, checkout = await BillingManager.async_checkout(order)
    if response.status == HTTPStatus.OK:
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={'message': checkout['url']}
        )

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={'message': 'checkout session error'}
    )
