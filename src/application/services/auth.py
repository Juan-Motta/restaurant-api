import logging

from src.domain.entities.auth import (
    AuthCreatePasswordInput,
    AuthLoginInput,
    AuthUserBase,
)
from src.domain.exceptions.auth import AuthenticationError
from src.domain.repositories.user import IUserRepository
from src.domain.utils.jwt import IJWTManager
from src.domain.utils.password import IPasswordManager

logger = logging.getLogger(__name__)


class AuthService:
    """
    A service class for handling user authentication and password management.

    This class provides methods to authenticate users, create password hashes,
    and generate authentication tokens. It utilizes a user repository and
    password utilities to perform secure operations.

    Attributes:
    -----------
    user_repository : IUserRepository
        An interface for user data access, allowing retrieval and updates of user information.

    password_utils : PasswordManager
        A utility class for managing password hashing and validation.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        password_manager: IPasswordManager,
        jwt_manager: IJWTManager,
    ):
        self.user_repository = user_repository
        self.password_manager = password_manager
        self.jwt_manager = jwt_manager

    async def authenticate(self, data: AuthLoginInput) -> AuthUserBase:
        """
        Authenticates a user based on their email and password.

        This method checks if a user exists with the given email, verifies
        the provided password against the stored password hash, and
        generates an authentication token if successful.

        Parameters:
        ----------
        email : str
            The email address of the user attempting to authenticate.

        password : str
            The plaintext password provided by the user.

        Returns:
        -------
        AuthUserBase
            An authenticated user object containing user information and an access token.

        Raises:
        -------
        AuthenticationError
            If the user is not found or if the provided password is invalid.
        """
        logger.info(f"Authenticating user with email {data.username}")

        if isinstance(data.username, int):
            user = await self.user_repository.get_by_id(user_id=data.username)
        else:
            user = await self.user_repository.get_by_email(email=data.username)

        if not user:
            raise AuthenticationError("User not found")
        if not user.is_active:
            raise AuthenticationError("User is not active")

        logger.info(f"Validating password for user with email {user.email}")

        user_password = await self.user_repository.get_password(user_id=user.id)

        is_valid_password = self.password_manager.verify_password(
            provided_password=data.password, stored_password=user_password
        )

        if not is_valid_password:
            raise AuthenticationError("Invalid password")

        logger.info(f"Generating token for user with email {user.email}")

        auth_user = AuthUserBase.model_validate(user, from_attributes=True)
        auth_user.access_token = self.jwt_manager.encode(user_id=user.id)

        logger.info(f"User with email {user.email} authenticated successfully")

        return auth_user

    async def create_password(self, data: AuthCreatePasswordInput) -> AuthUserBase:
        """
        Creates or updates the password for a specified user.

        This method retrieves the user by either their email or ID, hashes
        the provided password, and updates it in the user repository.

        Parameters:
        ----------
        user : AuthCreatePasswordInput
            An input object containing user information, including the new password.

        Returns:
        -------
        AuthUserBase
            The user object after the password has been created or updated.

        Raises:
        -------
        AuthenticationError
            If the user lookup fails.
        """
        logger.info(f"Creating password for user with email {data.username}")

        if isinstance(data.username, int):
            user = await self.user_repository.get_by_id(user_id=data.username)
        else:
            user = await self.user_repository.get_by_email(email=data.username)

        if not user:
            raise AuthenticationError("User not found")
        if user.is_active:
            raise AuthenticationError("User is already active")

        user_password = await self.user_repository.get_password(user_id=user.id)

        if user_password:
            raise AuthenticationError("Password already exists")

        hashed_password = self.password_manager.generate_password(data.password_1)

        user = await self.user_repository.update_password(
            user_id=user.id, password=hashed_password
        )

        logger.info(f"Password created for user with email {user.email}")

        return user
