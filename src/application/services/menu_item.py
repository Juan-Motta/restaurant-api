from src.domain.entities.menu_item import (
    MenuItemBase,
    MenuItemBaseInput,
    MenuItemWithRelations,
)
from src.domain.entities.pagination import Page, paginate
from src.domain.repositories.menu_item import IMenuItemRepository


class MenuItemService:
    def __init__(self, menu_item_repository: IMenuItemRepository):
        self.menu_item_repository = menu_item_repository

    async def get_all(
        self, page: int = 1, size: int = 10, filters: dict | None = None
    ) -> Page[MenuItemBase]:
        all_menu_items_count = await self.menu_item_repository.count_all()
        menu_items = await self.menu_item_repository.get_all(
            page=page, size=size, filters=filters
        )
        return paginate(
            data=menu_items, page=page, size=size, total=all_menu_items_count
        )

    async def get_by_id(self, menu_item_id: int) -> MenuItemWithRelations:
        return await self.menu_item_repository.get_by_id(menu_item_id)

    async def create(self, data: MenuItemBaseInput) -> MenuItemWithRelations:
        return await self.menu_item_repository.create(data)

    async def update(
        self, menu_item_id: int, data: MenuItemBaseInput
    ) -> MenuItemWithRelations:
        return await self.menu_item_repository.update(menu_item_id, data)

    async def deactivate(self, menu_item_id: int) -> MenuItemWithRelations:
        return await self.menu_item_repository.deactivate(menu_item_id)
