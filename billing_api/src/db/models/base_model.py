from sqlalchemy import Column, Integer

from db.base import Base

__all__ = (
    'BaseModel',
)


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    # id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
