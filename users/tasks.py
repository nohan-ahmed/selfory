# Create your tasks here
from celery import shared_task
from .utils import send_verification_email
import smtplib

@shared_task(bind=True, max_retries=5, default_retry_delay=300)
def send_email_task(self,subject: str, message: str, emails: list):
    try:
        send_verification_email(subject, message, emails)
    except smtplib.SMTPRecipientsRefused as exc:
        raise self.retry(exc=exc)