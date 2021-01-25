from django.db import models

# Create your models here.


class Store(models.Model):
    file = models.FileField(upload_to='')
