import logging

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.pagination import Page
from src.domain.entities.user import UserBase, UserBaseInput, UserWithRelations
from src.domain.filters.user import UserFilter
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.dependencies.services import get_user_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Users"])


@router.get("/users", response_model=Page[UserBase])
async def get_all_users(
    request: Request,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=0),
    session: AsyncSession = Depends(get_async_session),
    filters: UserFilter = Depends(UserFilter),
) -> Page[UserBase]:
    logger.info("Getting all users..")
    service = get_user_service(session=session)
    response = await service.get_all(
        page=page, size=size, filters=filters.model_dump(exclude_none=True)
    )
    return response


@router.get("/users/{user_id}", response_model=UserWithRelations)
async def get_user_by_id(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> UserWithRelations:
    logger.info(f"Getting user by id: {user_id}")
    service = get_user_service(session=session)
    response = await service.get_by_id(user_id)
    return response


@router.post("/users", response_model=UserWithRelations)
async def create_user(
    request: Request,
    data: UserBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> UserWithRelations:
    logger.info(f"Creating user: {data}")
    service = get_user_service(session=session)
    response = await service.create(data)
    return response


@router.put("/users/{user_id}", response_model=UserWithRelations)
async def update_user(
    request: Request,
    user_id: int,
    data: UserBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> UserWithRelations:
    logger.info(f"Updating user: {data}")
    service = get_user_service(session=session)
    response = await service.update(user_id, data)
    return response


@router.delete("/users/{user_id}", response_model=UserWithRelations)
async def deactivate_user(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(f"Deleting user by id: {user_id}")
    service = get_user_service(session=session)
    response = await service.deactivate(user_id)
    return response
