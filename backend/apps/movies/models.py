from django.db import models


class Movie(models.Model):
    """电影模型"""
    rank = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='豆瓣排名')
    title = models.CharField(max_length=255, db_index=True, verbose_name='电影名称')
    original_title = models.CharField(max_length=255, blank=True, verbose_name='原始标题')
    year = models.IntegerField(db_index=True, null=True, blank=True, verbose_name='上映年份')
    country = models.CharField(max_length=100, blank=True, verbose_name='国家/地区')
    director = models.CharField(max_length=255, blank=True, verbose_name='导演')
    cast = models.TextField(blank=True, verbose_name='主演')
    genres = models.CharField(max_length=100, blank=True, verbose_name='类型')
    runtime = models.IntegerField(null=True, blank=True, verbose_name='时长(分钟)')
    summary = models.TextField(blank=True, verbose_name='剧情简介')
    poster = models.ImageField(upload_to='posters/', verbose_name='海报图片')
    backdrop = models.ImageField(upload_to='backdrops/', null=True, blank=True, verbose_name='背景图片')
    douban_url = models.URLField(blank=True, verbose_name='豆瓣链接')
    douban_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='豆瓣评分')
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, verbose_name='本站平均评分')
    rating_count = models.IntegerField(default=0, verbose_name='本站评分人数')
    review_count = models.IntegerField(default=0, verbose_name='影评数量')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'movies_movie'
        verbose_name = '电影'
        verbose_name_plural = verbose_name
        ordering = ['rank']
        indexes = [
            models.Index(fields=['douban_rating']),
            models.Index(fields=['avg_rating']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title


class Genre(models.Model):
    """电影类型模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='类型名称')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL友好名称')

    class Meta:
        db_table = 'movies_genre'
        verbose_name = '电影类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
