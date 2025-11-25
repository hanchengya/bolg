from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    location = models.CharField(max_length=100, blank=True, verbose_name='所在地')
    website = models.URLField(blank=True, verbose_name='个人网站')
    follower_count = models.IntegerField(default=0, verbose_name='粉丝数')
    following_count = models.IntegerField(default=0, verbose_name='关注数')

    class Meta:
        db_table = 'users_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['date_joined']),
        ]

    def __str__(self):
        return self.username
