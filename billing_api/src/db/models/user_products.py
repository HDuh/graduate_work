from sqlalchemy import Column, Date, ForeignKey

from db.models import BaseModel

__all__ = (
    'UserProduct',
)


class UserProduct(BaseModel):
    __tablename__ = 'user_product'

    user_id = Column(ForeignKey('customer.user_id'))
    product_id = Column(ForeignKey('product.id'))
    expired_data = Column(Date(), nullable=True)
