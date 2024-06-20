from django.db import models
from pigeonwebapp.models import MailingList

class Email(models.Model):
    mail_to = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    send_at = models.DateTimeField()