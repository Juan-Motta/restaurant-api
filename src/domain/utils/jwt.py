from datetime import datetime


class IJWTManager:
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
        raise NotImplementedError
