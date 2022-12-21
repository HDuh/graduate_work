from src.core import OrderStatus
from src.db.models import Order
from src.schemas import OrderSchema
from .db_manager import DbManager

__all__ = (
    'OrderManager',
)


class OrderManager:

    @classmethod
    async def async_build_and_create(cls, user, product):
        """
        Сборка и создание заказа
        """
        order = Order(
            user_id=user.id,
            status=OrderStatus.UNPAID
        )
        order.product.append(product)
        await DbManager.async_save(order)
        return OrderSchema(
            customer_id=user.customer_id,
            price_id=product.price_stripe_id,
            quantity=1,
        )
