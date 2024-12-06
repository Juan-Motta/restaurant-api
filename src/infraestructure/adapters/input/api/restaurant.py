import logging

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dependencies.services import get_restaurant_service
from src.domain.filters.restaurant import RestaurantFilter
from src.infraestructure.adapters.outputs.db.session import get_async_session

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/restaurants")
async def get_all_restaurants(
    request: Request,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=0),
    session: AsyncSession = Depends(get_async_session),
    filters: RestaurantFilter = Depends(RestaurantFilter),
):
    logger.info("Getting all restaurants..")
    service = get_restaurant_service(session=session)
    response = await service.get_all(
        page=page, size=size, filters=filters.filter_criteria()
    )
    return response
