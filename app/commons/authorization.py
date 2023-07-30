import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

from jose import jwt

from app.config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class Session:
    user_id: int
    permissions: List[str]
    session_type: str
    extra: Optional[Dict] = None


def authorize(authorization_header: str) -> Optional[Session]:
    if not authorization_header:
        raise Exception("Invalid authorization header")

    bearer, jwt_encode = authorization_header.split(" ")

    if not (bearer == "Bearer" and jwt_encode):
        raise Exception("Invalid authorization header")

    jwt_decode = jwt.decode(
        jwt_encode,
        settings.SECRET_KEY,
        algorithms=settings.JWT_ALGORITHMS,
    )
    return Session(
        user_id=jwt_decode["user_id"],
        permissions=jwt_decode["permissions"],
        session_type=jwt_decode["session_type"],
        extra=jwt_decode["extra"],
    )
