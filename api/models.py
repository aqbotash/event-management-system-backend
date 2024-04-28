from django.db import models


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    img = models.ImageField(null=True, blank=True)   