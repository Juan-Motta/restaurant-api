from src.domain.entities.order_item import (
    OrderItemBase,
    OrderItemBaseInput,
    OrderItemWithRelations,
)


class IOrderItemRepository:
    async def count_all(self) -> int:
        raise NotImplementedError

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[OrderItemBase]:
        raise NotImplementedError

    async def get_by_id(self, order_item_id: int) -> OrderItemWithRelations | None:
        raise NotImplementedError

    async def create(self, data: OrderItemBaseInput) -> OrderItemWithRelations:
        raise NotImplementedError

    async def update(
        self, order_item_id: int, data: OrderItemBaseInput
    ) -> OrderItemWithRelations:
        raise NotImplementedError

    async def deactivate(self, order_item_id: int) -> OrderItemWithRelations:
        raise NotImplementedError
