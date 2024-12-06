from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infraestructure.commons.settings.base import settings

async_engine: AsyncEngine = create_async_engine(
    settings.DB_URL, echo=settings.DEBUG, future=True, pool_pre_ping=True
)

AsyncSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

sync_engine: Engine = create_engine(settings.DB_URL, echo=settings.DEBUG)

SyncSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_async_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@contextmanager
def get_sync_session():
    with SyncSessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
