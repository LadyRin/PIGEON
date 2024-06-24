import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pigeonproject.settings')

app = Celery('pigeonproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['pigeonwebapp'])

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from pigeonwebapp.tasks import check_queued_emails
    print("Setting up periodic tasks")
    sender.add_periodic_task(60.0, check_queued_emails.s(), name='check queued emails')