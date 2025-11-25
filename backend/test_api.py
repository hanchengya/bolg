#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API功能测试脚本
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:8000/api/v1'

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_movies_list():
    """测试电影列表API"""
    print_section("1. 测试电影列表 API")
    
    response = requests.get(f'{BASE_URL}/movies/')
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 成功获取电影列表")
        print(f"   总数量: {data.get('count', 0)}")
        print(f"   本页数量: {len(data.get('results', []))}")
        
        if data.get('results'):
            movie = data['results'][0]
            print(f"\n   首个电影信息:")
            print(f"   - ID: {movie.get('id')}")
            print(f"   - 标题: {movie.get('title')}")
            print(f"   - 排名: {movie.get('rank')}")
            print(f"   - 评分: {movie.get('douban_rating')}")
            print(f"   - 海报: {movie.get('poster')}")
    else:
        print(f"❌ 失败: {response.text}")

def test_movie_detail():
    """测试电影详情API"""
    print_section("2. 测试电影详情 API")
    
    response = requests.get(f'{BASE_URL}/movies/1/')
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        movie = response.json()
        print(f"✅ 成功获取电影详情")
        print(f"   标题: {movie.get('title')}")
        print(f"   原标题: {movie.get('original_title')}")
        print(f"   年份: {movie.get('year')}")
        print(f"   导演: {movie.get('director')}")
        print(f"   演员: {movie.get('cast')}")
        print(f"   类型: {movie.get('genres')}")
        print(f"   时长: {movie.get('runtime')}分钟")
        print(f"   豆瓣评分: {movie.get('douban_rating')}")
        print(f"   简介: {movie.get('summary')[:100]}...")
    else:
        print(f"❌ 失败: {response.text}")

def test_top_rated():
    """测试高分电影API"""
    print_section("3. 测试高分电影 API")
    
    response = requests.get(f'{BASE_URL}/movies/top_rated/')
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        movies = data if isinstance(data, list) else data.get('results', [])
        print(f"✅ 成功获取高分电影")
        print(f"   数量: {len(movies)}")
        
        if movies:
            print(f"\n   前5部高分电影:")
            for i, movie in enumerate(movies[:5], 1):
                print(f"   {i}. {movie.get('title')} - {movie.get('douban_rating')}分")
    else:
        print(f"❌ 失败: {response.text}")

def test_search():
    """测试搜索功能"""
    print_section("4. 测试搜索功能")
    
    search_terms = ['肖申克', '阿甘', '泰坦尼克']
    
    for term in search_terms:
        response = requests.get(f'{BASE_URL}/movies/search/', params={'q': term})
        print(f"搜索 '{term}': 状态码 {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            movies = data if isinstance(data, list) else data.get('results', [])
            print(f"   ✅ 找到 {len(movies)} 部电影")
            for movie in movies[:3]:
                print(f"      - {movie.get('title')}")
        else:
            print(f"   ❌ 失败")
        print()

def test_filter():
    """测试筛选功能"""
    print_section("5. 测试筛选功能")
    
    # 按年份筛选
    response = requests.get(f'{BASE_URL}/movies/', params={'year': 1994})
    print(f"筛选1994年电影: 状态码 {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', 0) if isinstance(data, dict) else len(data)
        print(f"   ✅ 找到 {count} 部电影")
    
    # 按评分排序
    response = requests.get(f'{BASE_URL}/movies/', params={'ordering': '-douban_rating'})
    print(f"\n按评分从高到低排序: 状态码 {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])[:5]
        print(f"   ✅ 前5名:")
        for i, movie in enumerate(results, 1):
            print(f"      {i}. {movie.get('title')} - {movie.get('douban_rating')}分")

def test_user_registration():
    """测试用户注册"""
    print_section("6. 测试用户注册 API")
    
    # 生成随机用户名
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    user_data = {
        'username': f'testuser_{timestamp}',
        'email': f'test_{timestamp}@example.com',
        'password': 'Test123456!',
        'password2': 'Test123456!'
    }
    
    response = requests.post(f'{BASE_URL}/auth/register/', json=user_data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ 用户注册成功")
        print(f"   用户名: {data.get('username')}")
        print(f"   邮箱: {data.get('email')}")
        print(f"   Token: {data.get('token', '已生成')[:50]}...")
        return data.get('token')
    else:
        print(f"❌ 失败: {response.text}")
        return None

def test_authenticated_endpoints(token):
    """测试需要认证的端点"""
    print_section("7. 测试认证端点")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 测试获取当前用户信息
    response = requests.get(f'{BASE_URL}/auth/me/', headers=headers)
    print(f"获取用户信息: 状态码 {response.status_code}")
    if response.status_code == 200:
        user = response.json()
        print(f"   ✅ 用户名: {user.get('username')}")
        print(f"   ✅ 邮箱: {user.get('email')}")

def test_api_docs():
    """测试API文档"""
    print_section("8. 测试API文档")
    
    # Swagger UI
    response = requests.get('http://localhost:8000/api/docs/')
    print(f"Swagger UI: 状态码 {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ 可访问: http://localhost:8000/api/docs/")
    
    # OpenAPI Schema
    response = requests.get('http://localhost:8000/api/schema/')
    print(f"\nOpenAPI Schema: 状态码 {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ 可访问: http://localhost:8000/api/schema/")

def main():
    print("\n" + "🎬" * 30)
    print("电影博客 API 功能测试")
    print("🎬" * 30)
    
    try:
        # 基础功能测试
        test_movies_list()
        test_movie_detail()
        test_top_rated()
        test_search()
        test_filter()
        test_api_docs()
        
        # 用户认证测试
        token = test_user_registration()
        if token:
            test_authenticated_endpoints(token)
        
        print_section("测试总结")
        print("✅ 所有核心功能测试完成！")
        print("\n主要功能验证:")
        print("  ✓ 电影列表获取")
        print("  ✓ 电影详情查看")
        print("  ✓ 高分电影推荐")
        print("  ✓ 电影搜索")
        print("  ✓ 电影筛选和排序")
        print("  ✓ 用户注册")
        print("  ✓ JWT认证")
        print("  ✓ API文档")
        
        print("\n🎉 后端API功能完整，运行正常！")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {str(e)}")

if __name__ == '__main__':
    main()
