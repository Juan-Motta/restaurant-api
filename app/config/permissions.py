# Standard Libraries
from typing import Any, Union

from strawberry.permission import BasePermission
from strawberry.types import Info

from starlette.requests import Request
from starlette.websockets import WebSocket

from app.commons.authorization import authorize

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context["request"]
        try:
            authorization_header = request.headers.get("Authorization")
            return authorize(authorization_header)
        except Exception as e:
            self.message = str(e)
            return False