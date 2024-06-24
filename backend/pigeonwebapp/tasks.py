from datetime import datetime, timezone, timedelta
from celery import shared_task
from django.core import mail
from pigeonwebapp.models.queued_email import QueuedEmail
import pytz
from pigeonproject import settings

@shared_task
def check_queued_emails():
    queued_emails = QueuedEmail.objects.all()
    for email in queued_emails:
        now = datetime.now(pytz.timezone(settings.TIME_ZONE))
        if email.send_at < now:
            send_queued_email(email)
            email.delete()


@shared_task
def send_queued_email(email: QueuedEmail):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            email.subject,
            email.message,
            'pigeon-events@lupm.in2p3.fr',
            [email.mail_to.address],
            connection=connection
        ).send()
