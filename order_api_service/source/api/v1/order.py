from http import HTTPStatus

from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()


@router.get('/ping', summary='Ping func')
async def ping_func() -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': 'ok'},
    )
