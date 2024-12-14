from sqlalchemy import func, select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session, joinedload

from src.domain.entities.order_item import (
    OrderItemBase,
    OrderItemBaseInput,
    OrderItemWithRelations,
)
from src.domain.repositories.order_item import IOrderItemRepository
from src.infraestructure.adapters.outputs.db.models import (
    MenuItemModel,
    OrderItemModel,
    OrderModel,
)


class OrderItemRepository(IOrderItemRepository):
    def __init__(self, session: Session):
        self.session = session

    async def count_all(self):
        query = select(func.count()).select_from(OrderItemModel)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[OrderItemBase]:
        query = select(OrderItemModel)
        if filters and filters.get("id"):
            query = query.where(OrderItemModel.id == filters.get("id"))
        if filters and filters.get("quantity_lte"):
            query = query.where(OrderItemModel.quantity <= filters.get("quantity_lte"))
        if filters and filters.get("quantity_gte"):
            query = query.where(OrderItemModel.quantity >= filters.get("quantity_gte"))
        if filters and filters.get("sub_total_lte"):
            query = query.where(
                OrderItemModel.sub_total <= filters.get("sub_total_lte")
            )
        if filters and filters.get("sub_total_gte"):
            query = query.where(
                OrderItemModel.sub_total >= filters.get("sub_total_gte")
            )
        if filters and filters.get("total_lte"):
            query = query.where(OrderItemModel.total <= filters.get("total_lte"))
        if filters and filters.get("total_gte"):
            query = query.where(OrderItemModel.total >= filters.get("total_gte"))
        if filters and filters.get("notes"):
            query = query.where(OrderItemModel.notes.ilike(f"%{filters.get('notes')}%"))
        if filters and filters.get("order_id"):
            query = query.where(OrderItemModel.order_id == filters.get("order_id"))
        if filters and filters.get("menu_item_id"):
            query = query.where(
                OrderItemModel.menu_item_id == filters.get("menu_item_id")
            )
        if filters and filters.get("is_active") in (True, False):
            query = query.where(OrderItemModel.is_active == filters.get("is_active"))
        if page:
            query = query.offset((page * size) - size)
        if size:
            query = query.limit(size)
        result = await self.session.execute(query)
        order_items = result.scalars().all()
        return [
            OrderItemBase.model_validate(order_item, from_attributes=True)
            for order_item in order_items
        ]

    async def get_by_id(self, order_item_id: int) -> OrderItemWithRelations | None:
        query = select(OrderItemModel).where(OrderItemModel.id == order_item_id)
        result = await self.session.execute(query)
        order_item = result.scalars().first()
        return (
            OrderItemWithRelations.model_validate(order_item, from_attributes=True)
            if order_item
            else None
        )

    async def create(self, order_item: OrderItemBaseInput) -> OrderItemWithRelations:
        order_item_model = OrderItemModel(**order_item.model_dump())
        self.session.add(order_item_model)
        await self.session.commit()
        order_item_model = await self.get_by_id(order_item_model.id)
        return OrderItemWithRelations.model_validate(
            order_item_model, from_attributes=True
        )

    async def update(
        self, order_item_id: int, order_item: OrderItemBaseInput
    ) -> OrderItemWithRelations:
        execute_update = (
            sql_update(OrderItemModel)
            .where(OrderItemModel.id == order_item_id)
            .values(**order_item.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        menu_item_model = await self.get_by_id(order_item_id)
        return OrderItemWithRelations.model_validate(
            menu_item_model, from_attributes=True
        )

    async def deactivate(self, order_item_id: int) -> OrderItemWithRelations:
        execute_update = (
            sql_update(OrderItemModel)
            .where(OrderItemModel.id == order_item_id)
            .values(is_active=False)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        order_item_model = await self.get_by_id(order_item_id)
        return OrderItemWithRelations.model_validate(
            order_item_model, from_attributes=True
        )
