from datetime import datetime, timedelta, timezone
from pigeonwebapp.models.queued_email import QueuedEmail
from pigeonwebapp.models.event import Event 
from django.template.loader import render_to_string


def register_emails_for_event(event: Event):
    # Create emails for event
    create_email_for_event(event, timedelta(minutes=5))
    create_email_for_event(event, timedelta(minutes=4))
    create_email_for_event(event, timedelta(minutes=2))
    create_email_for_event(event, timedelta(minutes=1))

def create_email_for_event(event: Event, time_before_event: timedelta):
    # Create email for event
    now = datetime.now(timezone(timedelta(hours=2)))
    event_date_time = datetime.combine(event.date, event.start_time)
    email_send_time = event_date_time - time_before_event
    email_send_time = timezone.make_aware(email_send_time)
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