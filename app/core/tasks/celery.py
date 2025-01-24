from celery import Celery

from app.config.config import settings

celery = Celery(
    __name__, broker=settings.CELERY_BROKER_URL, include=["app.core.cloud_provisioning"]
)
celery.conf.update(
    timezone="UTC",
)
