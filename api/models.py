from django.db import models

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to='events/', null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    dates = models.ManyToManyField('Date', related_name='events')  # ManyToMany link to Date model

    class Meta:
        unique_together = ('name', 'address')
    def __str__(self):
        return self.name

class Date(models.Model):
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.date:%Y-%m-%d %H:%M}"
