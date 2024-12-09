from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from src.infraestructure.adapters.outputs.repositories.restaurant import (
    RestaurantRepository,
)
from src.infraestructure.adapters.outputs.repositories.user import UserRepository
from src.infraestructure.dependencies.repositories import (
    get_restaurant_repository,
    get_user_repository,
)


@pytest.fixture
def mock_session():
    """Fixture to create a mock SQLAlchemy Session."""
    return MagicMock(spec=Session)


def test_get_restaurant_repository(mock_session):
    """Test the get_restaurant_repository function."""
    # Act
    repository = get_restaurant_repository(mock_session)

    # Assert
    assert isinstance(repository, RestaurantRepository)
    assert repository.session == mock_session  # Check that the session is set correctly


def test_get_user_repository(mock_session):
    """Test the get_user_repository function."""
    # Act
    repository = get_user_repository(mock_session)

    # Assert
    assert isinstance(repository, UserRepository)
    assert repository.session == mock_session  # Check that the session is set correctly
