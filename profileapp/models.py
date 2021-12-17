import sys
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from image_processing import thumbnail


class Profile(models.Model):
    owner = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    nickname = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    thumb = models.ImageField(upload_to='profile/thumbnail/', null=True)
    message = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 썸네일 생성 로직 필요
        self.generate_thumbnail()
        super().save(*args, **kwargs)

    def generate_thumbnail(self):
        """
        썸네일 생성 메서드
        """
        # 먼저 사용자가 이미지를 업로드했는지 확인
        if self.image:
            output = thumbnail.generate_thumbnail(self.image)

            # 장고에서 제공하는 메모리 내 이미지 파일을
            # 장고 파일 객체로 인식하게 도와주는 InMemoryUploadedFile 클래스를 이용해서
            # 이미지를 읽고, self.thumb 컬럼에 해당 변형된 이미지를 할당합니다
            self.thumb = InMemoryUploadedFile(output, 'ImageField', self.image.name,
                                              'image/jpeg', sys.getsizeof(output), None)


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(owner=instance, nickname='임시 닉네임')
