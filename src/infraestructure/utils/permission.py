import logging
from functools import wraps

from src.domain.exceptions.permission import PermissionError
from src.infraestructure.dependencies.services import get_permission_service
from src.infraestructure.utils.jwt import JWTManager

logger = logging.getLogger(__name__)


def permissions(
    action: str | None = None, owner: str | None = None, resource: str | None = None
):
    """
    Checks user permissions and enforces access control for the decorated function.

    This decorator validates the provided authorization token to ensure that
    the user has the necessary permissions before executing the decorated
    asynchronous function. If the token is missing or invalid, or if the user
    lacks the required permissions, a PermissionError is raised.

    Parameters
    ----------
    *args_1 : str
        A variable number of permission strings that specify the required
        permissions for accessing the decorated function.

    Returns
    -------
    Callable
        A wrapper function that performs permission checks and executes the
        decorated function if the checks pass.

    Raises
    ------
    PermissionError
        If the authorization token is missing, invalid, or if the user does
        not have the required permissions.

    Example
    -------
    @permissions("read:data", "write:data")
    async def my_secure_endpoint(request: Request, authorization: str = Header(None)):
        return {"message": "You have access to this endpoint!"}
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args_2, **kwargs_2):
            # Extract the authorization token and session from fastapi decorated
            # function arguments
            kwargs_2["context"] = {}
            session = kwargs_2["session"]
            authorization_token = kwargs_2["authorization"]

            # Check if the config defined in the decorator is valid (all parameters defined or none)
            if not (action and owner and resource) or not (
                not action and not owner and not resource
            ):
                raise ValueError("Invalid permissions")

            if action and owner and resource:
                required_permissions = f"{action}:{owner}:{resource}".upper()
            else:
                required_permissions = None

            # Initialize the JWT manager and permission service
            jwt_manager = JWTManager()
            permission_service = get_permission_service(session=session)

            authorization_payload = jwt_manager.decode(token=authorization_token)

            # If no authorization payload or required permissions are provided,
            # execute the decorated function
            if not authorization_payload and not required_permissions:
                return await func(*args_2, **kwargs_2)

            # If no authorization payload is provided, raise a PermissionError
            if not authorization_payload:
                raise PermissionError("Token not found")

            user_permissions = authorization_payload["permissions"]
            user_id = authorization_payload["user_id"]

            # Add the user ID and permissions to the context dictionary
            kwargs_2["context"]["user_id"] = user_id
            kwargs_2["context"]["permissions"] = user_permissions

            logger.info(f"Checking permissions for {user_id}")

            has_permissions = permission_service.has_permission(
                user_permissions=user_permissions,
                required_permissions=required_permissions,
            )

            # If the user has the required permissions, execute the decorated function
            if has_permissions:
                return await func(*args_2, **kwargs_2)

            raise PermissionError("Permission denied")

        return wrapper

    return decorator
