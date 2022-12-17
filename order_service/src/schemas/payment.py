from src.db.models import PaymentState

from src.schemas.base import BaseSchema


class PaymentSchema(BaseSchema):
    id: int
    invoice_id: str
    product_id: str
    user_id: str
    status: PaymentState

    class Config:
        orm_mode = True
        use_enum_values = True


class AddPaymentSchema(BaseSchema):
    user_id: str
    product_id: str
    amount: str
    currency: str = "RUB"


class NewPaymentSchema(BaseSchema):
    product: str
    currency: str = "RUB"


class UpdatePaymentSchema(BaseSchema):
    invoice_id: str
    status: PaymentState

    class Config:
        use_enum_values = True


class PaymentCancel(BaseSchema):
    user_id: str
    amount: int
    currency: str = "RUB"
