import logging
import jwt
from datetime import datetime, timezone, timedelta

from app.core.db import logger
from app.core.settings import Settings

settings = Settings()

ALGORITHM = "HS256"

logger = logging.getLogger(__name__)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth.expired_time)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.auth.secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.auth.secret, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (jwt.PyJWTError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        logger.error(f"Error decoding token: {str(e)}")
        return None
