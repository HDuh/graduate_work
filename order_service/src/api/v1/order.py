from http import HTTPStatus

from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.db import get_db_manager
from src.utils import security, get_token_payload

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get('/ping', summary='Ping func')
async def ping_func() -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': 'ok'},
    )


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.post('/create_order')
def create_order(product_id, access_token=Depends(security), db_manager=Depends(get_db_manager)):
    '''распаковать токен. проверить есть ли юзер у нас в бд. если есть, проверить есть ли активная подписка.
    если нет ...'''
    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if user := db_manager.async_get_user(user_id):
        ...
