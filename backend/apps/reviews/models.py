from django.db import models
from django.conf import settings


class Review(models.Model):
    """影评模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='reviews', verbose_name='用户')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE,
                              related_name='reviews', verbose_name='电影')
    title = models.CharField(max_length=255, verbose_name='影评标题')
    content = models.TextField(verbose_name='影评内容')
    contains_spoilers = models.BooleanField(default=False, verbose_name='包含剧透')
    helpful_count = models.IntegerField(default=0, verbose_name='有用数')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'reviews_review'
        verbose_name = '影评'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        unique_together = ['user', 'movie']  # 每个用户对每部电影只能写一篇影评
        indexes = [
            models.Index(fields=['movie', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} - {self.title}'


class Comment(models.Model):
    """评论模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='用户')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='影评')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='replies', verbose_name='父评论')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'reviews_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['review', 'created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.content[:30]}'
