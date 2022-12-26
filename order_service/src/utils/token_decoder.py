import uuid

import jwt
import logging

__all__ = (
    'get_token_payload'
)


def get_token_payload(token: str) -> dict:
    try:
        unverified_headers = jwt.get_unverified_header(token)
        # return jwt.decode(token, key=os.getenv('JWT_SECRET'), algorithms=unverified_headers["alg"])
        return {'user_id': uuid.uuid4()}  # Mock
    except Exception as _e:
        logging.error(f'Error JWT decode: {_e}')
        return {}
