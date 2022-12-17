import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum

from db.models import BaseModel

__all__ = (
    'Payment',
    'PaymentState',
)


class PaymentState(str, enum.Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    ERROR = "error"
    CANCELED = "canceled"


class Payment(BaseModel):
    __tablename__ = "payment"

    invoice_id = Column(Integer)
    # user_id
    product_id = Column(ForeignKey('product.id'))
    customer_id = Column(ForeignKey("customer.id"))
    state = Column(Enum(PaymentState))
