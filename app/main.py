from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import settings
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    from sqlalchemy import select

    from app.database.base import Session
    from app.models import User, UserProfile

    session = Session()
    # user = User(
    #     first_name="Jhon",
    #     last_name="Doe",
    #     email="jhon@example.com",
    #     nid="12345678",
    # )
    # user.set_password(password="12345678")
    # session.add(user)
    # session.commit()
    # query = select(User).select_from(User).where(User.id == 1)
    # user = session.execute(query).scalars().first()
    # print(user)
    # user_profile = UserProfile(
    #     user_id=user.id,
    #     profile=ProfileEnum.APP_ADMINISTRATOR
    # )
    # session.add(user_profile)
    # session.commit()
    # print(user.profiles)
    yield
    # shut down


app: FastAPI = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    dependencies=[],
)

app.include_router(router)
