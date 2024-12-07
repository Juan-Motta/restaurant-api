import logging

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dependencies.services import get_restaurant_service
from src.domain.entities.restaurant import (
    RestaurantBase,
    RestaurantBaseInput,
    RestaurantWithRelations,
)
from src.domain.filters.restaurant import RestaurantFilter
from src.infraestructure.adapters.outputs.db.session import get_async_session

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Restaurants"])


@router.get("/restaurants", response_model=list[RestaurantBase])
async def get_all_restaurants(
    request: Request,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=0),
    session: AsyncSession = Depends(get_async_session),
    filters: RestaurantFilter = Depends(RestaurantFilter),
) -> list[RestaurantBase]:
    logger.info("Getting all restaurants..")
    service = get_restaurant_service(session=session)
    response = await service.get_all(
        page=page, size=size, filters=filters.filter_criteria()
    )
    return response


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantWithRelations)
async def get_restaurant_by_id(
    request: Request,
    restaurant_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> RestaurantWithRelations:
    logger.info(f"Getting restaurant by id: {restaurant_id}")
    service = get_restaurant_service(session=session)
    response = await service.get_by_id(restaurant_id)
    return response


@router.post("/restaurants", response_model=RestaurantWithRelations)
async def create_restaurant(
    request: Request,
    data: RestaurantBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> RestaurantWithRelations:
    logger.info(f"Creating restaurant: {data}")
    service = get_restaurant_service(session=session)
    response = await service.create(data)
    return response


@router.put("/restaurants/{restaurant_id}", response_model=RestaurantWithRelations)
async def update_restaurant(
    request: Request,
    restaurant_id: int,
    data: RestaurantBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> RestaurantWithRelations:
    logger.info(f"Updating restaurant: {data}")
    service = get_restaurant_service(session=session)
    response = await service.update(restaurant_id, data)
    return response


@router.delete("/restaurants/{restaurant_id}", response_model=RestaurantWithRelations)
async def deactivate_restaurant(
    request: Request,
    restaurant_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(f"Deleting restaurant by id: {restaurant_id}")
    service = get_restaurant_service(session=session)
    response = await service.deactivate(restaurant_id)
    return response
