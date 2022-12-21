from src.core import OrderStatus
from src.db.models import Order
from src.schemas import OrderSchema
from .db_manager import get_db_manager

__all__ = (
    'OrderManager',
    'get_order_manager',
)


class OrderManager:

    @classmethod
    async def async_build_and_create(cls, user, product):
        order = Order(
            user_id=user.id,
            status=OrderStatus.UNPAID
        )
        order.product.append(product)
        db_manager = await get_db_manager()
        await db_manager.async_save(order)
        return OrderSchema(
            customer_id=user.customer_id,
            price_id=product.price_id,
            quantity=1,
        )


async def get_order_manager():
    return OrderManager
