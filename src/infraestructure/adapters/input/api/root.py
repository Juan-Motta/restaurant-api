from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.infraestructure.adapters.input.celery.dummy import dummy_task
from src.infraestructure.adapters.outputs.db.session import get_async_session
from src.infraestructure.utils.permission import permissions

router = APIRouter()


@router.get("/")
@permissions()
async def root(
    request: Request,
    authorization: str | None = Header(None),
    session: AsyncSession = Depends(get_async_session),
    context: dict = None,
):
    return {"message": "OK", "context": context}


@router.get("/dummy-task")
async def start_dummy_task():
    response = dummy_task.delay()
    return {"status": response.status, "task_id": response.id}
