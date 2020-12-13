from django.db import models
from ImageHandler import resize_upload
import time


class InShotsAds(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=160)
    image = models.ImageField()
    link = models.URLField()

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not InShotsAds.objects.exists():
            self.full_clean()
            super(InShotsAds, self).save(force_insert, force_update, using, update_fields)
        elif not InShotsAds.objects.exclude(pk=self.pk).exists():
            self.full_clean()
            super(InShotsAds, self).save(force_insert, force_update, using, update_fields)
        else:
            raise Exception('Only one model allowed')

        file_name = self.image.name.split('/')[-1]
        cdn_image = resize_upload(file_name, 'InShotsAds', str(self.id) + '_' + str(int(time.time())), (200, 200))
        if cdn_image is not None:
            self.image = cdn_image
            super(InShotsAds, self).save(force_insert, force_update, using, update_fields)
