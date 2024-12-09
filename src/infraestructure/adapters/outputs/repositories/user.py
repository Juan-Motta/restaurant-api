from sqlalchemy import func, select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session, joinedload

from src.domain.entities.user import UserBase, UserBaseInput, UserWithRelations
from src.domain.repositories.user import IUserRepository
from src.infraestructure.adapters.outputs.db.models import RestaurantModel, UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    async def count_all(self):
        query = (
            select(func.count())
            .select_from(UserModel)
            .where(UserModel.is_active == True)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[UserBase]:
        query = select(UserModel)
        if filters and filters.get("id"):
            query = query.where(UserModel.id == filters.get("id"))
        if filters and filters.get("first_name"):
            query = query.where(UserModel.name.ilike(f'%{filters.get("first_name")}%'))
        if filters and filters.get("last_name"):
            query = query.where(UserModel.name.ilike(f'%{filters.get("last_name")}%'))
        if filters and filters.get("is_active"):
            query = query.where(UserModel.is_active == filters.get("is_active"))
        if page:
            query = query.offset((page * size) - size)
        if size:
            query = query.limit(size)
        result = await self.session.execute(query)
        users = result.scalars().all()
        return [UserBase.model_validate(user, from_attributes=True) for user in users]

    async def get_by_id(self, user_id: int) -> UserWithRelations | None:
        query = (
            select(UserModel)
            .join(RestaurantModel, RestaurantModel.id == UserModel.restaurant_id)
            .options(joinedload(UserModel.restaurant))
            .where(UserModel.id == user_id)
        )
        result = await self.session.execute(query)
        user = result.scalars().first()
        return (
            UserWithRelations.model_validate(user, from_attributes=True)
            if user
            else None
        )

    async def create(self, user: UserBaseInput) -> UserWithRelations:
        user_model = UserModel(**user.model_dump())
        self.session.add(user_model)
        await self.session.commit()
        user_model = await self.get_by_id(user_model.id)
        return UserWithRelations.model_validate(user_model, from_attributes=True)

    async def update(self, user_id: int, user: UserBaseInput) -> UserWithRelations:
        execute_update = (
            sql_update(UserModel)
            .where(UserModel.id == user_id)
            .values(**user.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        user_model = await self.get_by_id(user_id)
        return UserWithRelations.model_validate(user_model, from_attributes=True)

    async def deactivate(self, user_id: int) -> UserWithRelations:
        execute_update = (
            sql_update(UserModel)
            .where(UserModel.id == user_id)
            .values(is_active=False)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        user_model = await self.get_by_id(user_id)
        return UserWithRelations.model_validate(user_model, from_attributes=True)
