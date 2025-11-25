#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.movies.models import Movie

print("验证电影数据修复情况：\n")
movies = Movie.objects.all()[:10]

for m in movies:
    title = m.title[:30] if len(m.title) > 30 else m.title
    country = m.country[:20] if m.country else "无"
    genres = m.genres[:30] if m.genres else "无"
    print(f"{m.rank}. {title}")
    print(f"   年份: {m.year}, 国家: {country}")
    print(f"   类型: {genres}\n")

# 统计有年份的电影数量
total = Movie.objects.count()
with_year = Movie.objects.filter(year__isnull=False).count()
print(f"总计: {total} 部电影")
print(f"有年份数据: {with_year} 部 ({with_year*100//total}%)")
print(f"缺少年份: {total - with_year} 部")
