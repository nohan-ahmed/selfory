from celery import shared_task
from jobs.utils import generate_content


@shared_task
def content_generation_task(job_id, prompt=None):
    generate_content(job_id, prompt)