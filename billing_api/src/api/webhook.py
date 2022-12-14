import stripe
from fastapi import APIRouter, Request

router = APIRouter()


@router.post('/')
async def webhook(request: Request):
    """ Отлавливает все события от stripe.
    Для работы с этой штукой нужно установить stripe cli.
    и прописать команду
    'stripe listen --forward-to=localhost:8001/api/webhook/'
     """
    json_data = await request.json()
    print('--' * 20)
    for k in json_data:
        print(k, json_data[k])
    print('--'*20)

    event = stripe.Event.construct_from(json_data, stripe.api_key)
    print(event.type)
    print('==='*20)
    return {'status': 'success'}
