from datetime import datetime

import stripe
from fastapi import APIRouter, Request, Depends

from src.core import SubscriptionStatus
from src.services.order import OrderService, get_order_service
from src.services.product import ProductService, get_product_service
from src.services.user import UserService, get_user_service

router = APIRouter()


@router.post('')
async def webhook(
        request: Request,
        order_service: OrderService = Depends(get_order_service),
        product_service: ProductService = Depends(get_product_service),
        user_service: UserService = Depends(get_user_service)):
    """ Отлавливает все события от stripe """
    json_data = await request.json()
    event = stripe.Event.construct_from(json_data, stripe.api_key)
    event_type = event['type']
    print('++++' * 20)
    # if event_type == 'checkout.session.completed':
    #     print(event_type)
    #     session = event['data']['object']
    #     # print(session)

    if event_type == 'payment_intent.succeeded':
        print(event_type)
        payment_intent_obj = event['data']['object']
        print(payment_intent_obj)

        customer_id = payment_intent_obj['customer']

        # find User
        user = await user_service.get_by_customer_id(customer_id)
        print(f'USER: {user.to_dict()}')

        status = payment_intent_obj['status']
        if status == 'succeeded':
            # update order status
            new_pay_intent_id = payment_intent_obj['id']
            updated_order = await order_service.update_order(user.id, new_pay_intent_id)
            print(f'Payment intent: {new_pay_intent_id}')
            if updated_order:
                print(f'UPD: {updated_order.to_dict()}')

    elif event_type == 'customer.subscription.updated':
        print(event_type)

        subscription_event = event['data']['object']
        customer_id = subscription_event['customer']

        print(subscription_event)
        product_stripe_id = subscription_event['plan']['product']
        canceled_at = subscription_event['canceled_at']
        user = await user_service.get_by_customer_id(customer_id)

        if not canceled_at:
            product = await product_service.get_product_by_product_stripe_id(product_stripe_id)

            start_date = datetime.utcfromtimestamp(subscription_event['current_period_start'])
            end_date = datetime.utcfromtimestamp(subscription_event['current_period_end'])

            subscription = await user_service.create_subscription(
                user_id=user.id,
                start=start_date,
                end=end_date,
                product_id=product.id
            )

            print(subscription)

        else:
            await user_service.update_subscription(user_id=user.id, status=SubscriptionStatus.INACTIVE)

    if event_type == 'customer.subscription.deleted':
        print(event_type)
        subscription_event = event['data']['object']
        customer_id = subscription_event['customer']
        if user := await user_service.get_by_customer_id(customer_id):
            await user_service.update_subscription(user.id, SubscriptionStatus.CANCELLED)
            print(f'Subscription for user [{user.id}] was canceled')

    # else:
    #     print('ANOTHER TYPE')
    #     print(event.type)
    #     event_data = event['data']['object']
    #
    #     print(event_data)
    # print('---' * 20)

    return {'status': 'success'}
