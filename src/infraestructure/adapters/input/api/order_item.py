import logging

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.order_item import (
    OrderItemBase,
    OrderItemBaseInput,
    OrderItemWithRelations,
)
from src.domain.entities.pagination import Page
from src.domain.filters.order_item import OrderItemFilter
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.dependencies.services import get_order_item_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Order Items"])


@router.get("/order-items", response_model=Page[OrderItemBase])
async def get_all_order_items(
    request: Request,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=0),
    session: AsyncSession = Depends(get_async_session),
    filters: OrderItemFilter = Depends(OrderItemFilter),
) -> Page[OrderItemBase]:
    logger.info("Getting all order items..")
    service = get_order_item_service(session=session)
    response = await service.get_all(
        page=page, size=size, filters=filters.model_dump(exclude_none=True)
    )
    return response


@router.get("/order-items/{order_item_id}", response_model=OrderItemWithRelations)
async def get_order_item_by_id(
    request: Request,
    order_item_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> OrderItemWithRelations:
    logger.info(f"Getting order item by id: {order_item_id}")
    service = get_order_item_service(session=session)
    response = await service.get_by_id(order_item_id)
    return response


@router.post("/order-items", response_model=OrderItemWithRelations)
async def create_order_item(
    request: Request,
    data: OrderItemBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> OrderItemWithRelations:
    logger.info(f"Creating order item: {data}")
    service = get_order_item_service(session=session)
    response = await service.create(data)
    return response


@router.put("/order-items/{order_item_id}", response_model=OrderItemWithRelations)
async def update_order_item(
    request: Request,
    order_item_id: int,
    data: OrderItemBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> OrderItemWithRelations:
    logger.info(f"Updating order item: {data}")
    service = get_order_item_service(session=session)
    response = await service.update(order_item_id, data)
    return response


@router.delete("/order-items/{order_item_id}", response_model=OrderItemWithRelations)
async def deactivate_order_item(
    request: Request,
    order_item_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> OrderItemWithRelations:
    logger.info(f"Deleting order item by id: {order_item_id}")
    service = get_order_item_service(session=session)
    response = await service.deactivate(order_item_id)
    return response
