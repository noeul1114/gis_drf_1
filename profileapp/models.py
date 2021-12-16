import sys
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


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
            # PILLOW 에서 제공하는 Image 클래스 이용 이미지를 열어줌
            img = Image.open(self.image)

            # 이미지 프로세싱 결과물을 임시저장해놓을 메모리를 할당
            output = BytesIO()

            # 원하는 이미지 사이즈로 이미지를 변형
            img = img.convert('RGB')
            img = img.resize((200, 200), Image.ANTIALIAS)

            # 이미지를 이전에 만든 메모리 공간에 저장
            img.save(output, format='JPEG', quality=95)

            # 이미지를 저장하면서 이동한 메모리 포인터를
            # 다시 첫번째 위치로 이동 (밑에 있는 InMemoryUploadedFile 에서
            # 이미지를 읽게 하도록 위함
            output.seek(0)

            # 장고에서 제공하는 메모리 내 이미지 파일을
            # 장고 파일 객체로 인식하게 도와주는 InMemoryUploadedFile 클래스를 이용해서
            # 이미지를 읽고, self.thumb 컬럼에 해당 변형된 이미지를 할당합니다
            self.thumb = InMemoryUploadedFile(output, 'ImageField', self.image.name,
                                              'image/jpeg', sys.getsizeof(output), None)


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(owner=instance, nickname='임시 닉네임')
