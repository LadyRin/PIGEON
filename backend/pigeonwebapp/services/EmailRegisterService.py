from datetime import datetime, timedelta, timezone
from pigeonwebapp.models.queued_email import QueuedEmail
from pigeonwebapp.models.event import Event 
from django.template.loader import render_to_string
from pigeonproject import settings
import pytz 


def register_emails_for_event(event: Event):
    # Remove all emails for event
    QueuedEmail.objects.filter(event=event).delete()

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

    email = QueuedEmail(event=event, send_at=email_send_time)
    email.save()