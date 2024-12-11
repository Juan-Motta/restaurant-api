from sqlalchemy import func, select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session, joinedload

from src.domain.entities.menu_item import (
    MenuItemBase,
    MenuItemBaseInput,
    MenuItemWithRelations,
)
from src.domain.repositories.menu_item import IMenuItemRepository
from src.infraestructure.adapters.outputs.db.models import (
    CategoryModel,
    MenuItemModel,
    RestaurantModel,
)


class MenuItemRepository(IMenuItemRepository):
    def __init__(self, session: Session):
        self.session = session

    async def count_all(self):
        query = select(func.count()).select_from(MenuItemModel)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[MenuItemBase]:
        query = select(MenuItemModel)
        if filters and filters.get("id"):
            query = query.where(MenuItemModel.id == filters.get("id"))
        if filters and filters.get("name"):
            query = query.where(MenuItemModel.name.ilike(f'%{filters.get("name")}%'))
        if filters and filters.get("is_active"):
            query = query.where(MenuItemModel.is_active == filters.get("is_active"))
        if page:
            query = query.offset((page * size) - size)
        if size:
            query = query.limit(size)
        result = await self.session.execute(query)
        menus = result.scalars().all()
        return [
            MenuItemBase.model_validate(menu, from_attributes=True) for menu in menus
        ]

    async def get_by_id(self, menu_item_id: int) -> MenuItemWithRelations | None:
        query = (
            select(MenuItemModel)
            .join(CategoryModel, CategoryModel.id == MenuItemModel.category_id)
            .options(joinedload(MenuItemModel.category))
            .join(RestaurantModel, RestaurantModel.id == MenuItemModel.restaurant_id)
            .options(joinedload(MenuItemModel.restaurant))
            .where(MenuItemModel.id == menu_item_id)
        )
        result = await self.session.execute(query)
        menu = result.scalars().first()
        return (
            MenuItemWithRelations.model_validate(menu, from_attributes=True)
            if menu
            else None
        )

    async def create(self, menu_item: MenuItemBaseInput) -> MenuItemWithRelations:
        menu_item_model = MenuItemModel(**menu_item.model_dump())
        self.session.add(menu_item_model)
        await self.session.commit()
        menu_item_model = await self.get_by_id(menu_item_model.id)
        return MenuItemWithRelations.model_validate(
            menu_item_model, from_attributes=True
        )

    async def update(
        self, menu_item_id: int, menu_item: MenuItemBaseInput
    ) -> MenuItemWithRelations:
        execute_update = (
            sql_update(MenuItemModel)
            .where(MenuItemModel.id == menu_item_id)
            .values(**menu_item.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        menu_item_model = await self.get_by_id(menu_item_id)
        return MenuItemWithRelations.model_validate(
            menu_item_model, from_attributes=True
        )

    async def deactivate(self, menu_item_id: int) -> MenuItemWithRelations:
        execute_update = (
            sql_update(MenuItemModel)
            .where(MenuItemModel.id == menu_item_id)
            .values(is_active=False)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        menu_item_model = await self.get_by_id(menu_item_id)
        return MenuItemWithRelations.model_validate(
            menu_item_model, from_attributes=True
        )
