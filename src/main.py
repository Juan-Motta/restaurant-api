import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infraestructure.commons.logger.base import setup_logging
from src.infraestructure.commons.settings.base import settings
from src.routes import METADATA, router_v1

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    dependencies=[],
    openapi_tags=METADATA,
)

app.include_router(router_v1)
