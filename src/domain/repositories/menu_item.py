from src.domain.entities.menu_item import (
    MenuItemBase,
    MenuItemBaseInput,
    MenuItemWithRelations,
)


class IMenuItemRepository:
    async def count_all(self) -> int:
        raise NotImplementedError

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[MenuItemBase]:
        raise NotImplementedError

    async def get_by_id(self, menu_item_id: int) -> MenuItemWithRelations | None:
        raise NotImplementedError

    async def create(self, data: MenuItemBaseInput) -> MenuItemWithRelations:
        raise NotImplementedError

    async def update(
        self, menu_item_id: int, data: MenuItemBaseInput
    ) -> MenuItemWithRelations:
        raise NotImplementedError

    async def deactivate(self, menu_item_id: int) -> MenuItemWithRelations:
        raise NotImplementedError
