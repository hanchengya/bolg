from django.db import models
from django.conf import settings


class Watchlist(models.Model):
    """观影清单模型"""
    STATUS_CHOICES = [
        ('want_to_watch', '想看'),
        ('watching', '在看'),
        ('watched', '已看'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='watchlist', verbose_name='用户')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, verbose_name='电影')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_watch',
                              verbose_name='状态')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    watched_at = models.DateTimeField(null=True, blank=True, verbose_name='观看时间')

    class Meta:
        db_table = 'watchlists_watchlist'
        verbose_name = '观影清单'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'movie']
        indexes = [
            models.Index(fields=['user', 'status', '-added_at']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} - {self.get_status_display()}'
