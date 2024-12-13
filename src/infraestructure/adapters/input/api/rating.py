import logging

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.pagination import Page
from src.domain.entities.rating import (
    RatingBase,
    RatingBaseInput,
    RatingWithRelations,
)
from src.domain.filters.rating import RatingFilter
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.dependencies.services import get_rating_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Menu Items"])


@router.get("/ratings", response_model=Page[RatingBase])
async def get_all_ratings(
    request: Request,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=0),
    session: AsyncSession = Depends(get_async_session),
    filters: RatingFilter = Depends(RatingFilter),
) -> Page[RatingBase]:
    logger.info("Getting all ratings..")
    service = get_rating_service(session=session)
    response = await service.get_all(
        page=page, size=size, filters=filters.filter_criteria()
    )
    return response


@router.get("/ratings/{rating_id}", response_model=RatingWithRelations)
async def get_rtings_by_id(
    request: Request,
    rating_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> RatingWithRelations:
    logger.info(f"Getting ratings by id: {rating_id}")
    service = get_rating_service(session=session)
    response = await service.get_by_id(rating_id)
    return response


@router.post("/ratings", response_model=RatingWithRelations)
async def create_rating(
    request: Request,
    data: RatingBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> RatingWithRelations:
    logger.info(f"Creating rating: {data}")
    service = get_rating_service(session=session)
    response = await service.create(data)
    return response


@router.put("/ratings/{rating_id}", response_model=RatingWithRelations)
async def update_rating(
    request: Request,
    rating_id: int,
    data: RatingBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> RatingWithRelations:
    logger.info(f"Updating rating: {data}")
    service = get_rating_service(session=session)
    response = await service.update(rating_id, data)
    return response


@router.delete("/ratings/{rating_id}", response_model=RatingWithRelations)
async def deactivate_rating(
    request: Request,
    rating_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> RatingWithRelations:
    logger.info(f"Deleting rating by id: {rating_id}")
    service = get_rating_service(session=session)
    response = await service.deactivate(rating_id)
    return response
