import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import billing, webhook
from src.core import settings

app = FastAPI(
    title=settings.app.project_name,
    docs_url='/billing/openapi',
    openapi_url='/billing/openapi.json',
    default_response_class=ORJSONResponse,
)


# app.mount("./static", StaticFiles(directory="static"), name="static")

@app.on_event('startup')
async def startup():
    ...


@app.on_event('shutdown')
async def shutdown():
    ...


app.include_router(billing.router, prefix='/api/v1/payment', tags=['Billing'])
app.include_router(webhook.router, prefix='/api/v1/payment/webhook', tags=['Webhook'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        reload=True,
        port=8001,
        log_config=settings.app.logging,
        log_level=logging.DEBUG,
    )
