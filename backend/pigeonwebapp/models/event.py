from django.db import models
from .event_theme import EventTheme
from .event_type import EventType
from .mailing_list import MailingList

class Event(models.Model):
    title = models.CharField(max_length=100)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    theme = models.ForeignKey(EventTheme, on_delete=models.CASCADE)
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    speaker_first_name = models.CharField(max_length=100)
    speaker_last_name = models.CharField(max_length=100)
    speaker_from = models.CharField(max_length=100)
    speaker_comment = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    attachment = models.FileField(upload_to='attachments/')