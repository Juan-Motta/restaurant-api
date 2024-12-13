import logging

from sqlalchemy.orm import Session

from src.celery import celery

logger = logging.getLogger(__name__)


@celery.task
def dummy_task() -> dict:
    logger.info("Dummy task executed")
    return {"status": "OK"}
