from django.db import models
from django.conf import settings


class Rating(models.Model):
    """评分模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='ratings', verbose_name='用户')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE,
                              related_name='ratings', verbose_name='电影')
    score = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='评分')  # 1.0 - 10.0 (豆瓣10分制)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评分时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'ratings_rating'
        verbose_name = '评分'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'movie']
        indexes = [
            models.Index(fields=['movie', 'score']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} - {self.score}'
