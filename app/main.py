from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import settings
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    yield
    # shut down


app: FastAPI = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    dependencies=[],
)

app.include_router(router)
