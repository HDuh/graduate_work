import logging
from uuid import UUID

from src.core import settings

__all__ = (
    'get_token_payload'
)


def get_token_payload(token: str = settings.app.test_user_id) -> dict:
    """ Mock для фронтенда """
    try:
        return {'user_id': UUID(token)}  # Mock
    except Exception as _e:
        logging.error(f'Error JWT decode: {_e}')
        return {}
