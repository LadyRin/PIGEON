from django.db import models

class MailingList(models.Model):
    name = models.CharField(max_length=100)
    address = models.EmailField()