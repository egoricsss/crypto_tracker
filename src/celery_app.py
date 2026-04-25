import os

from celery import Celery

# Set the default settings module for the 'celery' program.
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config")

# Create Celery app
celery_app = Celery(
    "crypto_tracker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

# Load configuration from environment variables with CELERY_ prefix
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
    task_soft_time_limit=240,  # 4 minutes soft limit
)

# Import beat schedule configuration
from celery_config import beat_schedule
from celery_config import timezone as scheduler_timezone

from app.price.tasks import fetch_deribit_prices

celery_app.conf.beat_schedule = beat_schedule
celery_app.conf.timezone = scheduler_timezone

# Auto-discover tasks from the app package
celery_app.autodiscover_tasks(["app"])
