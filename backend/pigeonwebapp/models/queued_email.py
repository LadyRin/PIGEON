from typing import Any
from django.db import models
from pigeonwebapp.models import MailingList

class QueuedEmail(models.Model):
    mail_to = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    send_at = models.DateTimeField()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)