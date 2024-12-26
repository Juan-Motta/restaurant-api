from sqlalchemy import select, union
from sqlalchemy.orm import Session

from src.domain.entities.permission import PermissionBase, RoleBase
from src.domain.repositories.permission import IPermissionRepository
from src.infraestructure.adapters.outputs.db.models import (
    PermissionModel,
    RoleModel,
    RolePermissionModel,
    UserPermissionModel,
    UserRoleModel,
)


class PermissionRepository(IPermissionRepository):
    def __init__(self, session: Session):
        self.session = session

    async def get_all_by_role_id(self, role_ids: list[int]):
        query = (
            select(PermissionModel)
            .join(
                RolePermissionModel,
                RolePermissionModel.permission_id == PermissionModel.id,
            )
            .join(RoleModel, RoleModel.id == RolePermissionModel.role_id)
            .join(UserRoleModel, UserRoleModel.role_id == RoleModel.id)
            .where(
                UserRoleModel.user_id.in_(role_ids),
                RoleModel.is_active == True,
                RolePermissionModel.is_active == True,
                PermissionModel.is_active == True,
                UserRoleModel.is_active == True,
            )
        )

        result = await self.session.execute(query)
        permissions = result.scalars().all()

        return [
            PermissionBase.model_validate(permission, from_attributes=True)
            for permission in permissions
        ]

    async def get_all_by_user_id(self, user_id: int):
        query_1 = (
            select(PermissionModel)
            .join(
                RolePermissionModel,
                RolePermissionModel.permission_id == PermissionModel.id,
            )
            .join(RoleModel, RoleModel.id == RolePermissionModel.role_id)
            .join(UserRoleModel, UserRoleModel.role_id == RoleModel.id)
            .where(
                UserRoleModel.user_id == user_id,
                RoleModel.is_active == True,
                RolePermissionModel.is_active == True,
                PermissionModel.is_active == True,
                UserRoleModel.is_active == True,
            )
        )
        query_2 = (
            select(PermissionModel)
            .join(
                UserPermissionModel,
                UserPermissionModel.permission_id == PermissionModel.id,
            )
            .where(
                UserPermissionModel.user_id == user_id,
                PermissionModel.is_active == True,
                UserPermissionModel.is_active == True,
                PermissionModel.is_active == True,
            )
        )
        combined_query = union(query_1, query_2)

        query = select(PermissionModel).from_statement(combined_query)

        result = await self.session.execute(query)
        permissions = result.scalars().all()

        return [
            PermissionBase.model_validate(permission, from_attributes=True)
            for permission in permissions
        ]

    async def get_roles_by_user_id(self, user_id: int):
        query = (
            select(RoleModel)
            .join(
                UserRoleModel,
                UserRoleModel.role_id == RoleModel.id,
            )
            .where(
                UserRoleModel.user_id == user_id,
                RoleModel.is_active == True,
                UserRoleModel.is_active == True,
            )
        )

        result = await self.session.execute(query)
        roles = result.scalars().all()

        return [RoleBase.model_validate(role, from_attributes=True) for role in roles]
