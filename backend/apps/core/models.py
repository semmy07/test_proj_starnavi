from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    city = models.CharField(max_length=64, default='', blank=True)
    country = models.CharField(max_length=64)
    phone = models.CharField(max_length=16, default='', blank=True)


class Post(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='creator', default=None)

    user_likes = models.ManyToManyField('User', blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    text = models.TextField(default='', blank=True)
