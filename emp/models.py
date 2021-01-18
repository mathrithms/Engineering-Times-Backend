from django.db import models
from ImageHandler import resize_upload
import time


class Company(models.Model):
    name = models.CharField(unique=True, max_length=60)
    logo = models.ImageField()

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Company, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

        file_name = self.logo.name.split('/')[-1]
        cdn_logo = resize_upload(file_name, 'Company', str(
            self.id) + '_' + str(int(time.time())), (50, 50))
        if cdn_logo is not None:
            self.logo = cdn_logo
            super(Company, self).save(force_insert,
                                      force_update, using, update_fields)

    class Meta:
        ordering = ['name', ]


class Intern(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name='internships')
    designation = models.CharField(max_length=100)
    link = models.URLField()
    expire = models.DateTimeField()

    class Meta:
        ordering = ['expire', ]


class Job(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name='jobs')
    designation = models.CharField(max_length=100)
    link = models.URLField()
    expire = models.DateTimeField()

    class Meta:
        ordering = ['expire', ]
