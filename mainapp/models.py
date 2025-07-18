from django.db import models

# Create your models here.

from django.db import models

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title