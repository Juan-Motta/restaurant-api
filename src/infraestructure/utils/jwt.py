import logging
from datetime import datetime, timedelta, timezone

import jwt

from src.infraestructure.commons.settings.base import settings

logger = logging.getLogger(__name__)


class JWTManager:
    @classmethod
    def encode(
        cls,
        user_id: int,
        roles: list[str] | None = None,
        permissions: list[str] | None = None,
        exp: datetime | None = None,
        nbf: datetime | None = None,
        iat: datetime | None = None,
    ) -> str:
        """
        Generates a JWT token for a given authenticated user.

        This method creates a JWT token with expiration, not before, and
        issued at claims, which encodes the user's ID and security details.

        Parameters:
        ----------
        user : AuthUserBase
            The authenticated user for whom the token is generated.

        Returns:
        -------
        str
            The generated JWT token as a string.
        """
        exp = exp or datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_EXPIRATION
        )
        nbf = nbf or datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_NOT_BEFORE
        )
        iat = iat or datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "roles": roles or [],
            "permissions": permissions or [],
            "exp": exp,
            "nbf": nbf,
            "iat": iat,
        }
        logger.info(f"Generating JWT token {payload} for user with ID {user_id}")
        token = jwt.encode(
            payload=payload, key=settings.JWT_SECRET_KEY, algorithm="HS256"
        )
        return token

    def decode(cls, token: str) -> dict:
        """
        Decodes a JWT token into its payload.

        This method decodes a given JWT token into its payload, which
        contains the user's ID and security details.

        Parameters:
        ----------
        token : str
            The JWT token to decode.

        Returns:
        -------
        dict
            The decoded payload of the JWT token.
        """
        try:
            payload = jwt.decode(
                jwt=token, key=settings.JWT_SECRET_KEY, algorithms="HS256"
            )
        except jwt.ExpiredSignatureError as e:
            logger.exception(e)
            payload = None
        except jwt.InvalidTokenError as e:
            logger.exception(e)
            payload = None
        return payload
