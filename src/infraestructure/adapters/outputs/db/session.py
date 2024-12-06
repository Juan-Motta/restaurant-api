from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infraestructure.commons.settings.base import settings

async_engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=settings.DEBUG, future=True, pool_pre_ping=True
)

session: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
