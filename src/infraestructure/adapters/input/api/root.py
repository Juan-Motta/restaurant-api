from fastapi import APIRouter

from src.infraestructure.adapters.input.celery.dummy import dummy_task

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "OK"}


@router.get("/dummy-task")
async def start_dummy_task():
    response = dummy_task.delay()
    return {"status": response.status, "task_id": response.id}
