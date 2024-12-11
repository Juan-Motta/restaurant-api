from src.domain.entities.order import OrderBase, OrderBaseInput, OrderWithRelations


class IOrderRepository:
    async def count_all(self) -> int:
        raise NotImplementedError

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[OrderBase]:
        raise NotImplementedError

    async def get_by_id(self, order_id: int) -> OrderWithRelations | None:
        raise NotImplementedError

    async def create(self, data: OrderBaseInput) -> OrderWithRelations:
        raise NotImplementedError

    async def update(self, order_id: int, data: OrderBaseInput) -> OrderWithRelations:
        raise NotImplementedError

    async def deactivate(self, order_id: int) -> OrderWithRelations:
        raise NotImplementedError
