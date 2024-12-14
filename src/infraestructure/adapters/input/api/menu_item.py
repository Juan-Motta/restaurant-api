import logging

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.menu_item import (
    MenuItemBase,
    MenuItemBaseInput,
    MenuItemWithRelations,
)
from src.domain.entities.pagination import Page
from src.domain.filters.menu_item import MenuItemFilter
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.dependencies.services import get_menu_item_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Menu Items"])


@router.get("/menu-items", response_model=Page[MenuItemBase])
async def get_all_menu_items(
    request: Request,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=0),
    session: AsyncSession = Depends(get_async_session),
    filters: MenuItemFilter = Depends(MenuItemFilter),
) -> Page[MenuItemBase]:
    logger.info("Getting all menu items..")
    service = get_menu_item_service(session=session)
    response = await service.get_all(
        page=page, size=size, filters=filters.model_dump(exclude_none=True)
    )
    return response


@router.get("/menu-items/{menu_item_id}", response_model=MenuItemWithRelations)
async def get_menu_item_by_id(
    request: Request,
    menu_item_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MenuItemWithRelations:
    logger.info(f"Getting menu item by id: {menu_item_id}")
    service = get_menu_item_service(session=session)
    response = await service.get_by_id(menu_item_id)
    return response


@router.post("/menu-items", response_model=MenuItemWithRelations)
async def create_menu_item(
    request: Request,
    data: MenuItemBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> MenuItemWithRelations:
    logger.info(f"Creating menu item: {data}")
    service = get_menu_item_service(session=session)
    response = await service.create(data)
    return response


@router.put("/menu-items/{menu_item_id}", response_model=MenuItemWithRelations)
async def update_menu_item(
    request: Request,
    menu_item_id: int,
    data: MenuItemBaseInput,
    session: AsyncSession = Depends(get_async_session),
) -> MenuItemWithRelations:
    logger.info(f"Updating menu item: {data}")
    service = get_menu_item_service(session=session)
    response = await service.update(menu_item_id, data)
    return response


@router.delete("/menu-items/{menu_item_id}", response_model=MenuItemWithRelations)
async def deactivate_menu_item(
    request: Request,
    menu_item_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MenuItemWithRelations:
    logger.info(f"Deleting menu item by id: {menu_item_id}")
    service = get_menu_item_service(session=session)
    response = await service.deactivate(menu_item_id)
    return response
