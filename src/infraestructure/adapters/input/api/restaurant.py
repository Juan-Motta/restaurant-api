from fastapi import APIRouter, Depends, Request

from src.infraestructure.adapters.outputs.db.session import get_async_session

router = APIRouter()


@router.get("/restaurants")
async def get_all_restaurants(request: Request, session=Depends(get_async_session)):
    return {"message": "OK"}
