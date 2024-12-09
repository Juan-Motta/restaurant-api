import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.infraestructure.adapters.outputs.db.base import Base
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.commons.settings.base import settings
from src.main import app  # type: ignore

TEST_DATABASE_URL: str = settings.DB_URL_TEST
main_app = app

# Create async engine
async_engine = create_async_engine(TEST_DATABASE_URL, echo=settings.DEBUG, future=True)

# Create an async sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="function")
async def app():
    """
    Create a fresh database for each test case
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    _app = main_app
    yield _app
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session(app: FastAPI):
    async_session = AsyncSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()


@pytest.fixture(scope="function")
async def client(app: FastAPI, db_session: AsyncSession):
    """
    Create a new TestClient of FastAPI that uses the `db_session`
    fixture to override the `get_async_session` dependency.
    """

    async def _get_test_db():
        return db_session

    app.dependency_overrides[get_async_session] = _get_test_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
