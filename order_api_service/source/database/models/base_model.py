from sqlalchemy import Column, Integer

from database.base import Base

__all__ = (
    'BaseModel',
)


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    def to_dict(self):
        column_names = self.__table__.columns.keys()
        return {column_i: getattr(self, column_i) for column_i in column_names}
