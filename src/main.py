import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infraestructure.adapters.input.api.root import router as root_router
from src.infraestructure.commons.logger.base import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI()

app.include_router(root_router)
