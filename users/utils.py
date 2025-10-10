from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings


def send_verification_email(subject: str, message: str, emails: list):
    send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, emails)
