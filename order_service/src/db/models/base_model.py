from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from src.db.base import Base

__all__ = (
    'BaseModel',
)


class BaseModel(Base):
    __abstract__ = True
    # TODO: Не генерится в моделях!
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4, autoincrement=True)

    def to_dict(self):
        column_names = self.__table__.columns.keys()
        return {column_i: getattr(self, column_i) for column_i in column_names}
