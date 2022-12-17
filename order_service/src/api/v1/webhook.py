import stripe
from fastapi import APIRouter, Request

router = APIRouter()


@router.post('')
async def webhook(request: Request):
    """ Отлавливает все события от stripe.
    Для работы с этой штукой нужно установить stripe cli.
    и прописать команду
    'stripe listen --forward-to=localhost:8001/api/webhook/'
     """
    json_data = await request.json()
    event = stripe.Event.construct_from(json_data, stripe.api_key)
    event_type = event['type']
    if 'invoice' in event_type or 'payment_intent' in event_type:
        print('=====' * 20)
        print(event_type)

    if event_type == 'checkout.session.completed':
        print(event.type)
        session = event['data']['object']
        if payment_link_id := session['payment_link']:
            payment_link = stripe.PaymentLink.retrieve(payment_link_id)
            payment_link_status = payment_link['active']

            print(f'Payment link status: {payment_link_status}')

            payment_link_utl = payment_link['url']

            stripe.PaymentLink.modify(
                payment_link_id,
                active=False,
            )
            print(f'Payment link url: {payment_link_utl} status: {payment_link_status}')
    #
    # elif event_type == 'payment_intent.created':
    #     payment_intent = event['data']['object']
    #     print(f'[{event.id}] PaymentIntent {payment_intent.id}: {payment_intent.status}')
    #
    # # if event_type == 'payment_intent.canceled':
    # #     payment_intent = event['data']['object']
    # #     print(f'[{event.id}] PaymentIntent {payment_intent.id}: {payment_intent.status}')
    # #
    # elif event_type == 'customer.updated':
    #     checkout_session = event['data']['object']
    #     print(checkout_session)
    #
    # elif event_type == 'payment_intent.succeeded':
    #     checkout_session = event['data']['object']
    #     print(f'checkout_session ID: {checkout_session.id}')
    #     print(checkout_session)
    #
    else:
        print('---' * 20)
        print('ANOTHER TYPE')
        print(event.type)
        print('---' * 20)

    return {'status': 'success'}
