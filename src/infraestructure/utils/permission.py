from fastapi import Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.dependencies.repositories import get_user_repository


class Permission:
    def __init__(
        self,
        permission: str,
        token: str = None,
    ):
        self.permission = permission

    def __call__(
        self,
        # authorization: str = Header(None),
        # session: AsyncSession = Depends(get_async_session)
    ):
        # user_repository = get_user_repository(session)
        print("Checking permission..")


def get_permission(
    permission: str | None = None,
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_async_session),
):
    return Permission(permission)
