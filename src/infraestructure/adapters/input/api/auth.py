import logging

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.auth import (
    AuthCreatePasswordInput,
    AuthLoginInput,
    AuthUserBase,
)
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.dependencies.services import get_auth_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Auth"])


@router.post("/auth/login")
async def login(
    request: Request,
    data: AuthLoginInput,
    session: AsyncSession = Depends(get_async_session),
) -> AuthUserBase:
    logger.info("Login user...")
    service = get_auth_service(session=session)
    response = await service.authenticate(data=data)
    return response


@router.post("/auth/password")
async def create_password(
    request: Request,
    data: AuthCreatePasswordInput,
    session: AsyncSession = Depends(get_async_session),
) -> AuthUserBase:
    logger.info("Creating user password...")
    service = get_auth_service(session=session)
    response = await service.create_password(data=data)
    return response
