from pydantic import BaseModel, Field


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
        return f"{self.action.lower()}:{self.owner.lower()}:{self.resource.lower()}"


class RoleBase(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    is_active: bool


class Context(BaseModel):
    user_id: int | None = None
    owners: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
