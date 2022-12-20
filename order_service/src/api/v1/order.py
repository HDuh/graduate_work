from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from src.services import DbManager, get_db_manager, StripeManager, get_stripe_manager
from src.db.base import get_session
from src.db.models import User
from src.core import SubscriptionStatus

router = APIRouter()


@router.post('/buy_product')
async def create_order(product_id: UUID,
                       db_manager: DbManager = Depends(get_db_manager),
                       stripe_manager: StripeManager = Depends(get_stripe_manager),
                       # session: AsyncSession = Depends(get_session),
                       # access_token=Depends(security),
                       ) -> JSONResponse:
    # token_payload = get_token_payload(access_token.credentials)
    # if not (user_id := token_payload.get('user_id')):
    #     raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    user_id = 'fcd1fe3e-364d-4428-b01e-0d5dae477b99'
    if not (user := await db_manager.async_get_by_id(User, user_id)):
        user = User(customer_id=stripe_manager.create_customer())
        await db_manager.async_save(user)

    user_subscription = await db_manager.async_get_user_subscription(user.id)
    if user_subscription and user_subscription.status == SubscriptionStatus.ACTIVE:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'message': f'user {user_id} already has an active subscription'}
        )



    # result = await order_service.create_order(product_id, user_id)
    # if not result:
    #     raise HTTPException(status_code=HTTPStatus.CONFLICT)

    # response, checkout = await billing_manager.async_checkout(result)
    # if response.status == HTTPStatus.OK:
    #     return JSONResponse(
    #         status_code=HTTPStatus.OK,
    #         content={'message': checkout['url']}
    #     )
    #
    # return JSONResponse(
    #     status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    #     content={'message': 'checkout session error'}
    # )
