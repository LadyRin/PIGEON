from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    upload_directory = models.CharField(max_length=100)
    port = models.IntegerField()
    