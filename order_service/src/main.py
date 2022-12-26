import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.staticfiles import StaticFiles

from src.api.v1 import order, webhook, product, subscription
from src.core import settings

app = FastAPI(
    title=settings.app.project_name,
    docs_url='/order/openapi',
    openapi_url='/order/openapi.json',
    default_response_class=ORJSONResponse,
)

this_directory = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(this_directory, "static")), name="static")


@app.on_event('startup')
async def startup():
    ...


@app.on_event('shutdown')
async def shutdown():
    ...


app.include_router(order.router, prefix='/api/v1/order', tags=['Order'])
app.include_router(product.router, prefix='/api/v1/product', tags=['Product'])
app.include_router(webhook.router, prefix='/api/v1/order/webhook', tags=['Webhook'])
app.include_router(subscription.router, prefix='/api/v1/subscription', tags=['Subscription'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        reload=True,
        port=8002,
        log_config=settings.app.logging,
        log_level=settings.app.log_level,
    )
