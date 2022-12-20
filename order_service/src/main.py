import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.staticfiles import StaticFiles

from src.api.v1 import order, webhook, product
from src.core import settings

app = FastAPI(
    title=settings.app.project_name,
    docs_url='/order/openapi',
    openapi_url='/order/openapi.json',
    default_response_class=ORJSONResponse,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.state.stripe_customer_id = None


@app.on_event('startup')
async def startup():
    ...


@app.on_event('shutdown')
async def shutdown():
    ...


app.include_router(order.router, prefix='/api/v1/order', tags=['Order'])
# app.include_router(product.router, prefix='/api/v1/product', tags=['Product'])
# app.include_router(webhook.router, prefix='/api/v1/webhook', tags=['Webhook'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        reload=True,
        port=8002,
        log_config=settings.app.logging,
        log_level=logging.DEBUG,
    )
