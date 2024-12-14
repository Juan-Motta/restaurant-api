import logging

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.order import OrderBase, OrderBaseInput, OrderWithRelations
from src.domain.entities.pagination import Page
from src.domain.filters.order import OrderFilter
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.dependencies.services import get_order_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Orders"])


@router.get("/orders", response_model=Page[OrderBase])
async def get_all_orders(
    request: Request,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=0),
    session: AsyncSession = Depends(get_async_session),
    filters: OrderFilter = Depends(OrderFilter),
) -> Page[OrderBase]:
    logger.info("Getting all orders..")
    service = get_order_service(session=session)
    response = await service.get_all(
        page=page, size=size, filters=filters.model_dump(exclude_none=True)
    )
    return response


@router.get("/orders/{order_id}", response_model=OrderWithRelations)
async def get_order_by_id(
    request: Request,
    order_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> OrderWithRelations:
    logger.info(f"Getting order by id: {order_id}")
    service = get_order_service(session=session)
    response = await service.get_by_id(order_id)
    return response


@router.post("/orders", response_model=OrderWithRelations)
async def create_order(
    request: Request,
    data: OrderBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> OrderWithRelations:
    logger.info(f"Creating order: {data}")
    service = get_order_service(session=session)
    response = await service.create(data)
    return response


@router.put("/orders/{order_id}", response_model=OrderWithRelations)
async def update_order(
    request: Request,
    order_id: int,
    data: OrderBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> OrderWithRelations:
    logger.info(f"Updating order: {data}")
    service = get_order_service(session=session)
    response = await service.update(order_id, data)
    return response


@router.delete("/orders/{order_id}", response_model=OrderWithRelations)
async def deactivate_order(
    request: Request,
    order_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(f"Deleting order by id: {order_id}")
    service = get_order_service(session=session)
    response = await service.deactivate(order_id)
    return response
