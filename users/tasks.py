# Create your tasks here
from celery import shared_task
from .utils import send_verification_email


@shared_task
def send_email_task(subject: str, message: str, emails: list):
    send_verification_email(subject, message, emails)
