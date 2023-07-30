from jose import jwt
from typing import List, Optional, Dict
from app.config.settings import settings
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Session:
    user_id: int
    permissions: List[str]
    session_type: str
    extra: Optional[Dict] = None
    

def authorize(authorization_header: str) -> Optional[Session]:
    if not authorization_header:
        return None

    bearer, jwt_encode = authorization_header.split(" ")

    if bearer == "Bearer" and jwt_encode:
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

    return None
