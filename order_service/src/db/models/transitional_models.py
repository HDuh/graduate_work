from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.db.base import Base

__all__ = (
    'order_product_table',
)

# Таблица связывает заказы и продукты
order_product_table = Table(
    'order_product',
    Base.metadata,
    Column('order_id', UUID(as_uuid=True), ForeignKey('order.id', ondelete="CASCADE")),
    Column('product_id', UUID(as_uuid=True), ForeignKey('product.id', ondelete="CASCADE")),
)
