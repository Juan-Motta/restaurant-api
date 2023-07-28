import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

DATABASE_URL: str = (
    "postgresql+psycopg://{user}:{password}@{host}:{port}/{name}".format(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        name=settings.DB_NAME,
    )
)

engine: Engine = create_engine(DATABASE_URL)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Session: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()
