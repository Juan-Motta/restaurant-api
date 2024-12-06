import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infraestructure.commons.logger.base import setup_logging
from src.routes import router_v1

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI()

app.include_router(router_v1)
