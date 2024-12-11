from src.domain.entities.order import OrderBase, OrderBaseInput, OrderWithRelations
from src.domain.entities.pagination import Page, paginate
from src.domain.repositories.order import IOrderRepository


class OrderService:
    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository

    async def get_all(
        self, page: int = 1, size: int = 10, filters: dict | None = None
    ) -> Page[OrderBase]:
        all_orders_count = await self.order_repository.count_all()
        restaurants = await self.order_repository.get_all(
            page=page, size=size, filters=filters
        )
        return paginate(data=restaurants, page=page, size=size, total=all_orders_count)

    async def get_by_id(self, order_id: int) -> OrderWithRelations:
        return await self.order_repository.get_by_id(order_id)

    async def create(self, data: OrderBaseInput) -> OrderWithRelations:
        return await self.order_repository.create(data)

    async def update(self, order_id: int, data: OrderBaseInput) -> OrderWithRelations:
        return await self.order_repository.update(order_id, data)

    async def deactivate(self, order_id: int) -> OrderWithRelations:
        return await self.order_repository.deactivate(order_id)
