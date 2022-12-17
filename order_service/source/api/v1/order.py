from http import HTTPStatus

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

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
