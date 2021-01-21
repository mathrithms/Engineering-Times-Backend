from django.db import models
from cropperjs.models import CropperImageField
# Create your models here.


def upload_location(instance, filename, **kwargs):
    file_path = 'blog/{title}/{filename}'.format(
        title=str(instance.title), filename=filename
    )
    return file_path


class Event(models.Model):
    title = models.CharField(max_length=100)
    time = models.DateTimeField()
    cost = models.PositiveSmallIntegerField()
    description = models.TextField(max_length=1000)
    link = models.URLField(max_length=200)
    image = CropperImageField(aspectratio=(1))
    organizers = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return str(self.title)


class Featured(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
