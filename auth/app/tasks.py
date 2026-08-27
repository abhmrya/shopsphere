from app.celery_app import celery_app
from app.services.email_service import send_welcome_email


@celery_app.task(name="send_welcome_email")
def send_welcome_email_task(
    to_email: str,
    first_name: str,
):
    send_welcome_email(
        to_email=to_email,
        first_name=first_name,
    )