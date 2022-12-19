from datetime import datetime

import stripe
from fastapi import APIRouter, Request, Depends

from src.services.order import OrderService, get_order_service
from src.services.product import ProductService, get_product_service
from src.services.subscription import SubscriptionService, get_subscription_service

router = APIRouter()


@router.post('')
async def webhook(
        request: Request,
        order_service: OrderService = Depends(get_order_service),
        product_service: ProductService = Depends(get_product_service),
        subscription_service: SubscriptionService = Depends(get_subscription_service)):
    """ Отлавливает все события от stripe """
    json_data = await request.json()
    event = stripe.Event.construct_from(json_data, stripe.api_key)
    event_type = event['type']
    print('++++' * 20)
    # if event_type == 'checkout.session.completed':
    #     print(event_type)
    #     session = event['data']['object']
    #     # print(session)

    # if event_type == 'payment_intent.succeeded':
    #     print(event_type)
    #     payment_intent_obj = event['data']['object']
    #     print(payment_intent_obj)
    #
    #     customer_id = payment_intent_obj['customer']
    #
    #     # find User
    #     user = await order_service.get_user_id_by_customer_id(customer_id)
    #     print(f'USER: {user.to_dict()}')
    #
    #     status = payment_intent_obj['status']
    #     if status == 'succeeded':
    #         # update order status
    #         new_pay_intent_id = payment_intent_obj['id']
    #         updated_order = await order_service.update_order(user.id, new_pay_intent_id)
    #         print(f'Payment intent: {new_pay_intent_id}')
    #         print(f'UPDATED order: {updated_order}')
    #         if updated_order:
    #             print(f'UPD: {updated_order.to_dict()}')
    #
    #         # delete unpaid orders for User by user ID
    #         # deleted_orders = await order_service.delete_unpaid_orders(user.id, new_pay_intent_id)
    #         # print(f'Deleted orders: {deleted_orders}')

    if event_type == 'customer.subscription.updated':
        print(event_type)
        subscription_event = event['data']['object']
        customer_id = subscription_event['customer']
        product_stripe_id = subscription_event['plan']['product']
        user = await order_service.get_user_id_by_customer_id(customer_id)
        product = await product_service.get_product_by_product_stripe_id(product_stripe_id)

        start_date = datetime.utcfromtimestamp(subscription_event['current_period_start'])
        end_date = datetime.utcfromtimestamp(subscription_event['current_period_end'])

        subscription = await subscription_service.create_subscription(
            user_id=user.id,
            start=start_date,
            end=end_date,
            product_id=product.id
        )

        print(subscription)

    # elif event_type == 'charge.succeeded':
    #     print(event_type)
    #     res = event['data']['object']
    #     print(res)
    # elif event_type == 'invoice.finalized':
    #     print(event_type)
    #     res = event['data']['object']
    #     print(res)


    # elif event_type == 'invoice.paid':
    #     print(event_type)
    #     res = event['data']['object']
    #     print(res)
    # elif event_type == 'invoice.payment_succeeded':
    #     print(event_type)
    #     res = event['data']['object']
    #     print(res)
    # else:
    #     print('ANOTHER TYPE')
    #     print(event.type)
    #
    # print('---' * 20)

    return {'status': 'success'}
