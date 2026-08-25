from celery import Celery

celery_app = Celery(
    "shopsphere",
    broker="redis://redis:6379/1",
    backend="redis://redis:6379/2",
)

celery_app.autodiscover_tasks(
    ["services.auth_service.app.workers"]
)