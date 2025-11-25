#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
导入豆瓣Top250电影数据到数据库
"""
import os
import sys
import json
import django
from pathlib import Path
import shutil
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 设置Django环境
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.movies.models import Movie, Genre
from django.core.files import File


def import_movies():
    """导入电影数据"""
    # JSON数据路径
    json_path = BASE_DIR.parent / 'douban_top250' / 'douban_top250.json'
    images_dir = BASE_DIR.parent / 'douban_top250' / 'images'

    if not json_path.exists():
        print(f"错误: 找不到数据文件 {json_path}")
        return

    print(f"开始导入豆瓣Top250电影数据...")
    print(f"数据文件: {json_path}")
    print(f"图片目录: {images_dir}")

    # 读取JSON数据（确保使用UTF-8编码）
    with open(json_path, 'r', encoding='utf-8-sig') as f:
        movies_data = json.load(f)

    print(f"找到 {len(movies_data)} 部电影")

    # 导入电影数据
    imported_count = 0
    updated_count = 0
    error_count = 0

    for item in movies_data:
        try:
            # 解析标题
            title_parts = item['title'].split(' / ')
            title = title_parts[0].strip()
            original_title = item['title'].strip()

            # 解析info字段
            info = item['info']
            director = ''
            cast = ''
            year = None
            country = ''
            genres = ''

            # 提取导演
            if '导演:' in info:
                director_part = info.split('导演:')[1].split('主演:')[0] if '主演:' in info else info.split('导演:')[1]
                director = director_part.strip().split('   ')[0].strip()

            # 提取主演和后续信息
            import re
            
            # 定义有效的电影类型关键词
            valid_genres = ['剧情', '爱情', '喜剧', '动作', '科幻', '动画', '悬疑', '惊悚', '恐怖', 
                          '犯罪', '奇幻', '冒险', '战争', '历史', '传记', '家庭', '儿童', '纪录片',
                          '短片', '音乐', '歌舞', '运动', '西部', '武侠', '古装', '灾难']
            
            # 定义国家/地区关键词（用于过滤）
            country_keywords = ['中国', '美国', '日本', '英国', '法国', '意大利', '德国', '韩国', 
                              '印度', '香港', '台湾', '大陆', '加拿大', '澳大利亚', '西班牙', '墨西哥']
            
            if '主演:' in info:
                cast_and_rest = info.split('主演:')[1]
                
                # 使用正则表达式查找年份（4位数字）
                year_match = re.search(r'(\d{4})', cast_and_rest)
                
                if year_match:
                    year = int(year_match.group(1))
                    # 主演部分在年份之前
                    cast_part = cast_and_rest[:year_match.start()]
                    # 清理主演信息，移除省略号和多余斜杠
                    cast = cast_part.replace('...', ' ').replace('/', ' ').strip()
                    
                    # 年份之后的信息是国家和类型
                    rest_info = cast_and_rest[year_match.end():].strip()
                    if rest_info.startswith('/'):
                        rest_info = rest_info[1:].strip()
                    
                    # 分割剩余部分并过滤
                    remaining_parts = [p.strip() for p in rest_info.split('/') if p.strip()]
                    
                    # 分离国家和类型
                    country_parts = []
                    genre_parts = []
                    
                    for part in remaining_parts:
                        # 跳过包含年份的部分（如"1964(中国大陆)"）
                        if re.search(r'\d{4}', part):
                            continue
                        
                        # 清理括号内容（如"(中国大陆)"）
                        part = re.sub(r'\([^)]*\)', '', part).strip()
                        if not part:
                            continue
                        
                        # 判断是国家还是类型
                        is_genre = any(keyword in part for keyword in valid_genres)
                        is_country = any(keyword in part for keyword in country_keywords)
                        
                        if is_genre and not is_country:
                            if part not in genre_parts:  # 去重
                                genre_parts.append(part)
                        elif is_country and not is_genre:
                            if part not in country_parts:  # 去重
                                country_parts.append(part)
                        elif not is_genre and not is_country:
                            # 如果两者都不是，默认作为国家
                            if part not in country_parts:  # 去重
                                country_parts.append(part)
                    
                    # 拼接结果
                    if country_parts:
                        country = ' '.join(country_parts)
                    if genre_parts:
                        genres = ' / '.join(genre_parts)
                else:
                    # 没有找到年份，整个作为主演
                    cast = cast_and_rest.strip()
            else:
                # 如果没有主演信息，直接从整个info中提取年份
                year_match = re.search(r'(\d{4})', info)
                if year_match:
                    year = int(year_match.group(1))

            # 创建或更新电影记录
            movie, created = Movie.objects.update_or_create(
                rank=int(item['rank']),
                defaults={
                    'title': title,
                    'original_title': original_title,
                    'year': year,
                    'country': country,
                    'director': director,
                    'cast': cast,
                    'genres': genres,
                    'summary': item.get('summary', ''),
                    'douban_url': item.get('detail_url', ''),
                    'douban_rating': float(item['rating']) if item.get('rating') else None,
                }
            )

            # 复制海报图片
            if item.get('local_image'):
                source_image = images_dir / item['local_image']
                if source_image.exists():
                    # 目标路径
                    dest_path = BASE_DIR / 'media' / 'posters' / item['local_image']
                    dest_path.parent.mkdir(parents=True, exist_ok=True)

                    # 复制文件
                    shutil.copy2(source_image, dest_path)

                    # 更新数据库中的路径
                    movie.poster = f"posters/{item['local_image']}"
                    movie.save()

            if created:
                imported_count += 1
                print(f"[{imported_count + updated_count}/{len(movies_data)}] 导入: {title}")
            else:
                updated_count += 1
                print(f"[{imported_count + updated_count}/{len(movies_data)}] 更新: {title}")

        except Exception as e:
            error_count += 1
            print(f"错误: 处理电影 {item.get('title', 'Unknown')} 时出错: {str(e)}")
            continue

    print("\n" + "=" * 60)
    print(f"导入完成!")
    print(f"新增电影: {imported_count} 部")
    print(f"更新电影: {updated_count} 部")
    print(f"错误数量: {error_count} 个")
    print(f"总计处理: {imported_count + updated_count} 部电影")
    print("=" * 60)


def create_genres():
    """创建电影类型数据"""
    print("\n创建电影类型...")

    genres_list = [
        '剧情', '爱情', '喜剧', '科幻', '动作', '悬疑', '犯罪',
        '惊悚', '冒险', '动画', '奇幻', '恐怖', '战争', '灾难',
        '西部', '传记', '歌舞', '武侠', '情色', '同性', '音乐',
        '家庭', '儿童', '历史', '运动', '黑色电影', '短片', '纪录片'
    ]

    created_count = 0
    for genre_name in genres_list:
        slug = genre_name.lower().replace(' ', '-')
        genre, created = Genre.objects.get_or_create(
            name=genre_name,
            defaults={'slug': slug}
        )
        if created:
            created_count += 1

    print(f"创建了 {created_count} 个电影类型")


if __name__ == '__main__':
    print("=" * 60)
    print("豆瓣Top250电影数据导入工具")
    print("=" * 60)

    # 创建电影类型
    create_genres()

    # 导入电影数据
    import_movies()

    print("\n全部完成!")
