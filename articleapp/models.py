import sys

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

# Create your models here.
from image_processing import thumbnail


class Article(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='article', null=True)

    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='article/', null=False)
    thumb = models.ImageField(upload_to='article/thumbnail/', null=True)
    content = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.generate_thumbnail()
        super().save(*args, **kwargs)

    def generate_thumbnail(self):
        if self.image:
            output = thumbnail.generate_thumbnail(self.image)
            self.thumb = InMemoryUploadedFile(output, 'ImageField', self.image.name,
                                              'image/jpeg', sys.getsizeof(output), None)
