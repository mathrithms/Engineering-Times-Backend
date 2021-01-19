from django.db import models

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
    image = models.ImageField(
        upload_to=upload_location, null=False, blank=True)
    organizers = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


class Featured(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
