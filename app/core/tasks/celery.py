"""
This module is used to create a Celery instance and configure it with the Celery broker URL.

The Celery instance is used to run asynchronous tasks in the application, more specifically,
to create cloud resources for a shop in the background. See `app.core.cloud_provisioning`.
"""

from celery import Celery

from app.config.config import settings

celery = Celery(
    __name__, broker=settings.CELERY_BROKER_URL, include=["app.core.cloud_provisioning"]
)
celery.conf.update(timezone="UTC", worker_redirect_stdouts=False)
