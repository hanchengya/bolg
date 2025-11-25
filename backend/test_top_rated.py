#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.movies.models import Movie
from apps.movies.serializers import MovieListSerializer

print("开始测试 top_rated 查询...")

# 执行与视图相同的查询
movies = Movie.objects.filter(
    douban_rating__isnull=False
).filter(
    douban_rating__gte=9.0
).only(
    'id', 'rank', 'title', 'year', 'poster', 
    'douban_rating', 'avg_rating', 'rating_count', 
    'review_count', 'genres'
).order_by('-douban_rating')[:10]

print(f"查询结果: {movies.count()} 部电影")

# 尝试序列化
try:
    serializer = MovieListSerializer(movies, many=True)
    data = serializer.data
    print(f"序列化成功! 数据长度: {len(data)}")
    print(f"第一部电影: {data[0]['title'] if data else 'None'}")
except Exception as e:
    print(f"序列化失败: {e}")
    import traceback
    traceback.print_exc()
