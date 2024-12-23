import logging

from celery import Celery
from src.infraestructure.commons.settings.base import settings

# Initialize Celery
celery: Celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL,
)
celery.conf.worker_send_task_events = True
celery.conf.task_send_sent_event = True
celery.conf.task_track_started = True
celery.conf.result_extended = True
celery.conf.enable_utc = True

# Auto-discover tasks
celery.autodiscover_tasks(["src.infraestructure.adapters.input.celery.dummy"])

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Set Celery's logger to DEBUG
celery_logger = logging.getLogger("celery")
celery_logger.setLevel(logging.DEBUG)
