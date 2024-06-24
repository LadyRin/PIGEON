from typing import Any
from django.db import models
from pigeonwebapp.models import Event

class QueuedEmail(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    send_at = models.DateTimeField()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)