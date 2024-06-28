from datetime import datetime, timezone, timedelta
from celery import shared_task
from django.core import mail
from pigeonwebapp.models.queued_email import QueuedEmail
import pytz
from pigeonproject import settings
from django.template.loader import render_to_string
from pigeonwebapp.models import Server
from pigeonwebapp.services.server import upload_file
from pigeonwebapp.services.events import check_for_updates, generate_json
from pigeonwebapp.models import Event

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
    address = email.event.mailing_list.address

    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject,
            message,
            'pigeon-events@lupm.in2p3.fr',
            [address],
            connection=connection
        ).send()

@shared_task
def update_servers_with_json(force=False):
    file_path = 'events.json'

    if force:
        generate_json(file_path)
    elif not check_for_updates():
        print("No changes to events. Skipping update.")
        return
    
    servers = Server.objects.all()
    print(f"Updating {len(servers)} servers with JSON file.")
    for server in servers:
        upload_file(server, file_path)