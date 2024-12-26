from pydantic import BaseModel


class PermissionBase(BaseModel):
    id: int
    name: str
    resource: str
    owner: str
    action: str
    description: str | None = None
    is_active: bool

    @property
    def permission(self):
        return f"{self.resource.lower()}:{self.action.lower()}:{self.owner.lower()}"


class RoleBase(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    is_active: bool
