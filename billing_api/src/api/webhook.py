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
    event = stripe.Event.construct_from(json_data, stripe.api_key)

    if event['type'] == 'checkout.session.completed':
        print(event.type)
        session = event['data']['object']
        print(session)
        print('===' * 20)

    else:
        print('ANOTHER TYPE')
        print(event.type)

    return {'status': 'success'}
