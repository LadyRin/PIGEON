from datetime import datetime, timezone, timedelta
from celery import shared_task
from django.core import mail
from pigeonwebapp.models.queued_email import QueuedEmail
import pytz
from pigeonproject import settings
from django.template.loader import render_to_string

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

    subject = f"Event reminder: {email.event.title}"

    context = {
        'title': email.event.title,
        'description': email.event.description,
        'date': email.event.date,
        'start_time': email.event.start_time,
        'end_time': email.event.end_time,
    }

    message = render_to_string('reminder_email.txt', context)
    address = email.event.mailing_list.email

    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject,
            message,
            'pigeon-events@lupm.in2p3.fr',
            [address],
            connection=connection
        ).send()
