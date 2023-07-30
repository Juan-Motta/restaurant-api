from fastapi import APIRouter

from app.graphql import router as graphql_router

router: APIRouter = APIRouter()

router.include_router(graphql_router, prefix="/api/v1/graphql")
