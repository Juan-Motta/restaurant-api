from src.domain.entities.order_item import (
    OrderItemBase,
    OrderItemBaseInput,
    OrderItemWithRelations,
)
from src.domain.entities.pagination import Page, paginate
from src.domain.repositories.order_item import IOrderItemRepository


class OrderItemService:
    def __init__(self, order_item_repository: IOrderItemRepository):
        self.order_item_repository = order_item_repository

    async def get_all(
        self, page: int = 1, size: int = 10, filters: dict | None = None
    ) -> Page[OrderItemBase]:
        all_order_items_count = await self.order_item_repository.count_all()
        order_items = await self.order_item_repository.get_all(
            page=page, size=size, filters=filters
        )
        return paginate(
            data=order_items, page=page, size=size, total=all_order_items_count
        )

    async def get_by_id(self, order_item_id: int) -> OrderItemWithRelations:
        return await self.order_item_repository.get_by_id(order_item_id)

    async def create(self, data: OrderItemBaseInput) -> OrderItemWithRelations:
        return await self.order_item_repository.create(data)

    async def update(
        self, order_item_id: int, data: OrderItemBaseInput
    ) -> OrderItemWithRelations:
        return await self.order_item_repository.update(order_item_id, data)

    async def deactivate(self, order_item_id: int) -> OrderItemWithRelations:
        return await self.order_item_repository.deactivate(order_item_id)
