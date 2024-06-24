from datetime import datetime, timedelta, timezone
from pigeonwebapp.models.queued_email import QueuedEmail
from pigeonwebapp.models.event import Event 
from django.template.loader import render_to_string
from pigeonproject import settings
import pytz 


def register_emails_for_event(event: Event):
    # Create emails for event
    create_email_for_event(event, timedelta(minutes=5))
    create_email_for_event(event, timedelta(minutes=4))
    create_email_for_event(event, timedelta(minutes=2))
    create_email_for_event(event, timedelta(minutes=1))

def create_email_for_event(event: Event, time_before_event: timedelta):
    # Create email for event
    tz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(tz)
    event_date_time = datetime.combine(event.date, event.start_time)
    event_date_time = tz.localize(event_date_time)
    email_send_time = event_date_time - time_before_event
    if email_send_time < now:
        return

    context = {
        'title': event.title,
        'description': event.description,
        'date': event.date,
        'start_time': event.start_time,
        'end_time': event.end_time,
    }

    message = render_to_string('reminder_email.txt', context)

    email = QueuedEmail(mail_to=event.mailing_list, subject='Rappel ' + event.title, message=message, send_at=email_send_time)
    email.save()