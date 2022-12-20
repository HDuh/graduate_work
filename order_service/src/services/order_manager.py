from src.db.models import Order
from src.core import OrderStatus


class OrderManager:

    @classmethod
    async def async_build_and_create(cls, user, product):
        order = Order(
            user=user.id,
            status=OrderStatus.UNPAID
        )
        order.product.append(product)
        db_manager.async_save(order)
        return


def get_order_manager():
    return OrderManager
