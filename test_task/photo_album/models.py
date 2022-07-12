import os
import shutil
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Person(User):
    class Meta:
        proxy = True

    @receiver(post_save, sender=User)
    def add_user_dir(sender, instance, created, **kwargs):
        if created:
            os.mkdir(f"photo_album/static/images/user_{instance.id}")

    @receiver(post_delete, sender=User)
    def delete_user_dir(sender, instance, **kwargs):
        shutil.rmtree(f"photo_album/static/images/user_{instance.id}")


class Album(models.Model):
    name = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",)

class Photo(models.Model):
    name = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, verbose_name='Альбом')

class Tag(models.Model):
    photo = models.ForeignKey('Album', on_delete=models.CASCADE, verbose_name=' Тег')
    name = models.CharField(max_length=255)