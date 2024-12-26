import logging
from functools import wraps

from src.domain.exceptions.permission import PermissionError
from src.infraestructure.dependencies.services import get_permission_service
from src.infraestructure.utils.jwt import JWTManager

logger = logging.getLogger(__name__)


def _validate_permissions_config(
    action: str | None, owner: str | None, resource: str | None
):
    """
    Validates the configuration of permissions parameters.

    This function checks that either all of the action, owner, and resource
    parameters are provided or none one of them are defined. If the
    parameters are not in a valid state, a ValueError is raised.

    Parameters
    ----------
    action : str | None
        The action associated with the permission. Can be None.

    owner : str | None
        The owner of the resource. Can be None.

    resource : str | None
        The resource that the action will be applied to. Can be None.

    Raises
    ------
    ValueError
        If the parameters do not meet the validation criteria.
    """
    all_params_defined = (
        action is not None and owner is not None and resource is not None
    )
    no_params_defined = not (action is None and owner is None and resource is None)

    if not all_params_defined or not no_params_defined:
        raise ValueError("Invalid permissions configuration")


def _format_required_permissions(action: str, owner: str, resource: str) -> str:
    """
    Formats required permissions into a standardized string.

    This function generates a string representing the required permissions
    in the format "ACTION:OWNER:RESOURCE", with all characters
    converted to uppercase. If any of the parameters are not provided,
    None is returned instead.

    Parameters
    ----------
    action : str
        The action that needs permission.

    owner : str
        The owner of the resource.

    resource : str
        The resource that the action will be applied to.

    Returns
    -------
    str | None
        A formatted permission string in uppercase or None if parameters are missing.
    """
    if action and owner and resource:
        required_permissions = f"{action}:{owner}:{resource}".upper()
    else:
        required_permissions = None
    return required_permissions


def _validate_token_format(token: str) -> str:
    """
    Validates the format of the provided token.

    This function checks if the token follows the Bearer token format.
    It extracts the authorization token from the provided string,
    ensuring it adheres to the expected structure. If the format is
    incorrect, a PermissionError is raised.

    Parameters
    ----------
    token : str
        The authorization token in the format "Bearer <token>".

    Returns
    -------
    str
        The extracted authorization token part.

    Raises
    ------
    PermissionError
        If the token does not have a valid format or is missing the token part.
    """
    token_type, authorization_token = token.split(" ")
    if token_type.lower() != "bearer":
        raise PermissionError("Invalid token type")
    if not authorization_token:
        raise PermissionError("Invalid authorization token")
    return authorization_token


def _get_token_payload(token: str) -> dict:
    """
    Decodes the provided JWT token to extract its payload.

    This function uses a JWT manager to decode the token and retrieve
    the payload. If the token is invalid or the payload cannot be
    retrieved, a PermissionError is raised.

    Parameters
    ----------
    token : str
        The authorization token to decode.

    Returns
    -------
    dict
        The payload contained in the decoded token.

    Raises
    ------
    PermissionError
        If the token is invalid or its payload cannot be fetched.
    """
    jwt_manager = JWTManager()
    authorization_payload = jwt_manager.decode(token=token)

    if not authorization_payload:
        raise PermissionError("Invalid authorization token")

    return authorization_payload


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
            kwargs_2["context"] = {}
            session = kwargs_2["session"]
            authorization_token = kwargs_2["authorization"]

            _validate_permissions_config(action, owner, resource)
            required_permissions = _format_required_permissions(action, owner, resource)

            if required_permissions is not None and not authorization_token:
                raise PermissionError("Token not found")

            if required_permissions is None and authorization_token is None:
                return await func(*args_2, **kwargs_2)

            authorization_token = _validate_token_format(authorization_token)
            authorization_payload = _get_token_payload(authorization_token)

            user_permissions = authorization_payload["permissions"]
            user_id = authorization_payload["user_id"]

            kwargs_2["context"]["user_id"] = user_id
            kwargs_2["context"]["permissions"] = user_permissions
            kwargs_2["context"]["roles"] = authorization_payload["roles"]

            logger.info(f"Checking permissions for {user_id}")

            permission_service = get_permission_service(session=session)
            has_permissions = permission_service.has_permission(
                user_permissions=user_permissions,
                required_permissions=required_permissions,
            )

            if has_permissions:
                return await func(*args_2, **kwargs_2)

            raise PermissionError("Permission denied")

        return wrapper

    return decorator
