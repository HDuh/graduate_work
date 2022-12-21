from pydantic import BaseModel

__all__ = (
    'MessageResponse',
)


class MessageResponse(BaseModel):
    message: str
