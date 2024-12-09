from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from src.application.services.restaurant import RestaurantService
from src.application.services.user import UserService
from src.infraestructure.dependencies.services import (
    get_restaurant_service,
    get_user_service,
)


@pytest.fixture
def mock_session():
    """Fixture to mock a SQLAlchemy Session."""
    return MagicMock(spec=Session)


def test_get_restaurant_service(mock_session):
    # Arrange
    mock_repo = MagicMock()
    # Mock the repository function to return the mock repository
    with patch(
        "src.infraestructure.dependencies.services.get_restaurant_repository",
        return_value=mock_repo,
    ):
        # Act
        service = get_restaurant_service(mock_session)

        # Assert
        assert isinstance(service, RestaurantService)
        assert service.restaurant_repository == mock_repo


def test_get_user_service(mock_session):
    # Arrange
    mock_user_repo = MagicMock()
    # Mock the user repository function to return the mock repository
    with patch(
        "src.infraestructure.dependencies.services.get_user_repository",
        return_value=mock_user_repo,
    ):
        # Act
        service = get_user_service(mock_session)

        # Assert
        assert isinstance(service, UserService)
        assert service.user_repository == mock_user_repo
