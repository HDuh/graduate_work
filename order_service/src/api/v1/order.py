from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.order import OrderCreate
from src.services.order import get_order_service, OrderService

router = APIRouter()


# templates = Jinja2Templates(directory="templates")


# @router.get('/')
# def index(request: Request):
#     return templates.TemplateResponse('index.html', {'request': request})


@router.post('/create_order',
             response_model=OrderCreate,
             status_code=HTTPStatus.CREATED)
async def create_order(product_id=uuid4(),
                       # access_token=Depends(security),
                       order_service: OrderService = Depends(get_order_service)) -> OrderCreate:
    # token_payload = get_token_payload(access_token.credentials)
    # if not (user_id := token_payload.get('user_id')):
    #     raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    user_id = 'fcd1fe3e-364d-4428-b01e-0d5dae477b99'

    result = await order_service.create_order(product_id, user_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)

    return result
