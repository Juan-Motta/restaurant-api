from sqlalchemy import func, select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session, joinedload

from src.domain.entities.order import OrderBase, OrderBaseInput, OrderWithRelations
from src.domain.repositories.order import IOrderRepository
from src.infraestructure.adapters.outputs.db.models import (
    OrderModel,
    RestaurantModel,
    UserModel,
)


class OrderRepository(IOrderRepository):
    def __init__(self, session: Session):
        self.session = session

    async def count_all(self):
        query = select(func.count()).select_from(OrderModel)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[OrderBase]:
        query = select(OrderModel)
        if filters and filters.get("id"):
            query = query.where(OrderModel.id == filters.get("id"))
        if filters and filters.get("status"):
            query = query.where(OrderModel.status == filters.get("status"))
        if filters and filters.get("total_amount_lte"):
            query = query.where(
                OrderModel.total_amount <= filters.get("total_amount_lte")
            )
        if filters and filters.get("total_amount_gte"):
            query = query.where(
                OrderModel.total_amount >= filters.get("total_amount_gte")
            )
        if filters and filters.get("delivery_address"):
            query = query.where(
                OrderModel.delivery_address.ilike(
                    f'%{filters.get("delivery_address")}%'
                )
            )
        if filters and filters.get("special_instructions"):
            query = query.where(
                OrderModel.special_instructions.ilike(
                    f'%{filters.get("special_instructions")}%'
                )
            )
        if filters and filters.get("estimated_delivery_time_lte"):
            query = query.where(
                OrderModel.estimated_delivery_time
                <= filters.get("estimated_delivery_time_lte")
            )
        if filters and filters.get("estimated_delivery_time_gte"):
            query = query.where(
                OrderModel.estimated_delivery_time
                >= filters.get("estimated_delivery_time_gte")
            )
        if filters and filters.get("restaurant_id"):
            query = query.where(
                OrderModel.restaurant_id == filters.get("restaurant_id")
            )
        if filters and filters.get("customer_id"):
            query = query.where(OrderModel.customer_id == filters.get("customer_id"))
        if filters and filters.get("is_active") in (True, False):
            query = query.where(OrderModel.is_active == filters.get("is_active"))
        if page:
            query = query.offset((page * size) - size)
        if size:
            query = query.limit(size)
        result = await self.session.execute(query)
        orders = result.scalars().all()
        return [
            OrderBase.model_validate(order, from_attributes=True) for order in orders
        ]

    async def get_by_id(self, order_id: int) -> OrderWithRelations | None:
        query = select(OrderModel).where(OrderModel.id == order_id)
        result = await self.session.execute(query)
        order = result.scalars().first()
        return (
            OrderWithRelations.model_validate(order, from_attributes=True)
            if order
            else None
        )

    async def create(self, order: OrderBaseInput) -> OrderWithRelations:
        order_model = OrderModel(**order.model_dump())
        self.session.add(order_model)
        await self.session.commit()
        order_model = await self.get_by_id(order_model.id)
        return OrderWithRelations.model_validate(order_model, from_attributes=True)

    async def update(self, order_id: int, order: OrderBaseInput) -> OrderWithRelations:
        execute_update = (
            sql_update(OrderModel)
            .where(OrderModel.id == order_id)
            .values(**order.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        order_model = await self.get_by_id(order_id)
        return OrderWithRelations.model_validate(order_model, from_attributes=True)

    async def deactivate(self, order_id: int) -> OrderWithRelations:
        execute_update = (
            sql_update(OrderModel)
            .where(OrderModel.id == order_id)
            .values(is_active=False)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        order_model = await self.get_by_id(order_id)
        return OrderWithRelations.model_validate(order_model, from_attributes=True)
