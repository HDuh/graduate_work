from functools import lru_cache
from uuid import uuid4

from fastapi import Depends

from src.core import SubscriptionStatus, OrderStatus
from src.db import get_db_manager, DbManager, StripeManager
from src.db.models import Product, User, Order
from src.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    async def create_order(self, product_id, user_id):

        if not (user := await self.db_manager.get_by_id(User, user_id)):
            customer = StripeManager.create_customer()
            user = User(id=user_id, customer_id=customer['id'])
            await self.db_manager.add(user)

        if not user.subscription or user.subscription.status == SubscriptionStatus.INACTIVE:
            product = await self.db_manager.get_by_id(Product, product_id)
            payment_intent = StripeManager.create_payment_intent(product)
            new_order = Order(
                id=uuid4(),
                user_id=user.id,
                pay_intent_id=payment_intent['id'],
                status=OrderStatus.UNPAID,
            )

            new_order.product.append(product)
            await self.db_manager.add(new_order)

            return OrderCreate(customer_id=user.customer_id,
                               price_id=product.price_stripe_id,
                               quantity=1)

            # TODO: передать заказ в сервис оплаты (передачу можно реализовать на фронте)


@lru_cache()
def get_order_service(db_manager: DbManager = Depends(get_db_manager)) -> OrderService:
    return OrderService(db_manager)
