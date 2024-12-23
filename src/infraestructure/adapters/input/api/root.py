from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import UserBase
from src.infraestructure.adapters.input.celery.dummy import dummy_task
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.utils.permission import get_permission

router = APIRouter()


@router.get("/")
async def root(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: UserBase = Depends(get_permission("root:read")),
):
    return {"message": "OK"}


@router.get("/dummy-task")
async def start_dummy_task():
    response = dummy_task.delay()
    return {"status": response.status, "task_id": response.id}
