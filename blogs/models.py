from django.db import models
from ImageHandler import resize_upload
import time


class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    profile = models.URLField()

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Author, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['id', ]


class Blog(models.Model):
    title = models.CharField(max_length=60)
    abstract = models.TextField()
    thumbnail = models.ImageField()
    main_image = models.ImageField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='blogs')
    importance = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-importance', '-timestamp']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, cdn_thumbnail=None):
        self.full_clean()
        super(Blog, self).save(force_insert, force_update, using, update_fields)
        file_name = self.thumbnail.name.split('/')[-1]
        cdn_thumbnail = resize_upload(file_name, 'BlogThumbnail', str(self.id) + '_' + str(int(time.time())), (80, 45))
        if cdn_thumbnail is not None:
            self.thumbnail = cdn_thumbnail

        file_name = self.main_image.name.split('/')[-1]
        cdn_main_image = resize_upload(file_name, 'BlogMain', str(self.id) + '_' + str(int(time.time())))
        if cdn_main_image is not None:
            self.main_image = cdn_main_image

        if cdn_main_image is not None or cdn_thumbnail is not None:
            super(Blog, self).save(force_insert, force_update, using, update_fields)


class ContentBlock(models.Model):
    text = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.PROTECT, related_name='contentBlock')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(ContentBlock, self).save(force_insert, force_update, using, update_fields)

        file_name = self.image.name.split('/')[-1]
        cdn_image = resize_upload(file_name, 'ContentBlock', str(self.id) + '_' + str(int(time.time())))
        if cdn_image is not None:
            self.image = cdn_image
            super(ContentBlock, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['id', ]


class Reference(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    blog = models.ForeignKey(Blog, on_delete=models.PROTECT, related_name='references')

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(Reference, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['id', ]


class Recommended(models.Model):
    tier1 = models.ForeignKey(Blog, on_delete=models.PROTECT, related_name='tier1')
    tier1_image = models.ImageField()
    tier2 = models.ForeignKey(Blog, on_delete=models.PROTECT, related_name='tier2')
    tier2_image = models.ImageField()
    tier3 = models.ForeignKey(Blog, on_delete=models.PROTECT, related_name='tier3')
    tier3_image = models.ImageField()
    tier4 = models.ForeignKey(Blog, on_delete=models.PROTECT, related_name='tier4')
    tier4_image = models.ImageField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not Recommended.objects.exists():
            self.full_clean()
            super(Recommended, self).save(force_insert, force_update, using, update_fields)
        elif not Recommended.objects.exclude(pk=self.pk).exists():
            self.full_clean()
            super(Recommended, self).save(force_insert, force_update, using, update_fields)
        else:
            raise Exception('Only one model allowed')

        file_name = self.tier1_image.name.split('/')[-1]
        new_tier_1_image = resize_upload(file_name, 'recommended', 'T1_' + str(int(time.time())), (400, 400))
        if new_tier_1_image is not None:
            self.tier1_image = new_tier_1_image

        file_name = self.tier2_image.name.split('/')[-1]
        new_tier_2_image = resize_upload(file_name, 'recommended', 'T2_' + str(int(time.time())), (400, 200))
        if new_tier_2_image is not None:
            self.tier2_image = new_tier_2_image

        file_name = self.tier3_image.name.split('/')[-1]
        new_tier_3_image = resize_upload(file_name, 'recommended', 'T3_' + str(int(time.time())), (200, 200))
        if new_tier_3_image is not None:
            self.tier3_image = new_tier_3_image

        file_name = self.tier4_image.name.split('/')[-1]
        new_tier_4_image = resize_upload(file_name, 'recommended', 'T4_' + str(int(time.time())), (200, 200))
        if new_tier_4_image is not None:
            self.tier4_image = new_tier_4_image

        super(Recommended, self).save(force_insert, force_update, using, update_fields)
