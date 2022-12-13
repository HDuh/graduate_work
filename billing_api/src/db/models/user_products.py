from sqlalchemy import Column, Integer, Date, ForeignKey

from db.models import BaseModel

__all__ = (
    'UserProduct',
)


class UserProduct(BaseModel):
    __tablename__ = 'user_product'

    user_id = Column(Integer, ForeignKey('customer.user_id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    # product_type =
    expired_data = Column(Date(), nullable=True)
