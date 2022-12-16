from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


__all__ = (
    'order_product_table',
)


# Таблица связывает заказы и продукты
order_product_table = Table(
    'order_product',
    Column('order_id', UUID(as_uuid=True), ForeignKey('order.id')),
    Column('product_id', UUID(as_uuid=True), ForeignKey('product.id')),
)
