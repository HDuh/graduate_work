import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps retuns bytes, but pydantic requires unicode
    return orjson.dumps(v, default=default).decode()


class BaseMixin(BaseModel):
    class Config:
        orm_mode = True

    class Meta:
        # Replace default lib for json to faster orjson
        json_loads = orjson.loads
        json_dumps = orjson_dumps
