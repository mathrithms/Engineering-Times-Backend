from django.db import models
from ImageHandler import resize_upload
import time


class Category(models.Model):
    title = models.CharField(max_length=20, unique=True)
    importance = models.IntegerField(default=0)

    class Meta:
        ordering = ['-importance', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Category, self).save(*args, **kwargs)


class Shots(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField(max_length=200)
    image = models.ImageField()
    link = models.URLField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='shots'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    importance = models.IntegerField(default=0)
    is_recommended = models.BooleanField(default=True)

    class Meta:
        ordering = ['-importance', '-timestamp']

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Shots, self).save(force_insert,
                                force_update, using, update_fields)

        file_name = self.image.name.split('/')[-1]
        cdn_image = resize_upload(file_name, 'shots', str(
            self.id) + '_' + str(int(time.time())), (200, 200))
        if cdn_image is not None:
            self.image = cdn_image
            super(Shots, self).save(force_insert,
                                    force_update, using, update_fields)
