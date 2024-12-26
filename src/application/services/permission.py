from src.domain.repositories.permission import IPermissionRepository


class PermissionService:
    def __init__(self, permission_repository: IPermissionRepository):
        self.permission_repository = permission_repository

    async def has_permission(
        self, user_permissions: list[str], required_permissions: list[str]
    ) -> bool:
        if not required_permissions:
            return True
        else:
            return bool(set(user_permissions) & set(required_permissions))
