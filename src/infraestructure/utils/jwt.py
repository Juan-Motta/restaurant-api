from datetime import datetime, timedelta, timezone

import jwt

from src.infraestructure.commons.settings.base import settings


class JWTManager:
    @classmethod
    def encode(
        cls,
        user_id: int,
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
        exp = exp or datetime.now(timezone.utc) + timedelta(hours=1)
        nbf = nbf or datetime.now(timezone.utc) + timedelta(hours=1)
        iat = iat or datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "exp": exp,
            "nbf": nbf,
            "iat": iat,
        }
        token = jwt.encode(payload=payload, key="secret", algorithm="HS256")
        return token
