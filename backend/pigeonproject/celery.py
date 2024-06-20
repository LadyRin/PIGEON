import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pigeonproject.settings')

app = Celery('pigeonproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['pigeonwebapp'])

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

@app.task
def test(arg):
    print(arg)