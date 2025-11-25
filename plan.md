# 电影博客网站设计方案

> **数据库配置**: 本项目使用MySQL数据库
> **地址**: 10.5.80.8:3306 | **用户**: root | **密码**: 123456

## 📌 项目概述

### 项目背景
基于豆瓣Top250电影数据，打造一个现代化的电影博客社区平台，允许用户注册、发布影评、评分、收藏电影，并通过卡片瀑布流的方式展示电影内容。

### 项目目标
- 🎬 展示豆瓣Top250电影资源（已有250部电影数据和海报）
- 👥 构建活跃的电影爱好者社区
- 💬 提供优质的影评和讨论平台
- 📱 提供现代化、响应式的用户体验

### 核心特性
1. **电影展示系统** - 卡片瀑布流布局，支持搜索和多维度筛选
2. **评论评分系统** - 用户可发表影评并为电影打分
3. **个人收藏系统** - 观影清单、想看/在看/已看标记、自定义片单
4. **用户社交功能** - 关注其他用户，查看动态
5. **用户注册发布** - 任何注册用户都可以发布影评和创建内容

---

## 🎯 用户角色与权限

### 角色定义

| 角色 | 权限 | 说明 |
|------|------|------|
| **游客** | 浏览电影、查看评论、搜索筛选 | 未登录用户，只读权限 |
| **注册用户** | 游客权限 + 发布影评、评分、收藏、关注、创建片单 | 普通用户，核心用户群 |
| **管理员** | 所有权限 + 管理电影数据、审核内容、管理用户 | 内容管理和维护 |

### 用户注册流程
```
访问网站 → 点击注册 → 填写信息(用户名/邮箱/密码)
→ 邮箱验证(可选) → 完善个人资料 → 开始使用
```

### 内容发布流程
```
登录 → 浏览电影详情页 → 点击"写影评"
→ 填写标题和内容 → 选择是否包含剧透 → 发布
```

---

## 🏗️ 技术架构

### 技术栈选型

#### 后端技术栈
- **框架**: Django 4.2 LTS
- **API**: Django REST Framework 3.14+
- **数据库**: MySQL 8.0+ (地址: 10.5.80.8:3306)
- **缓存**: Redis 7+
- **异步任务**: Celery + Redis
- **认证**: JWT (djangorestframework-simplejwt)
- **图片处理**: Pillow
- **API文档**: drf-spectacular (OpenAPI 3.0)

#### 前端技术栈
- **框架**: Vue.js 3 (Composition API)
- **构建工具**: Vite 5+
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **UI组件**: Tailwind CSS 3 + Flowbite Vue
- **HTTP客户端**: Axios
- **瀑布流**: vue-masonry-css
- **图片懒加载**: Intersection Observer API

#### 开发工具
- **版本控制**: Git
- **代码规范**: ESLint + Prettier (前端), Black + isort (后端)
- **API测试**: Postman / Thunder Client
- **调试**: Vue DevTools, Django Debug Toolbar

### 项目结构

```
movie-blog/
│
├── backend/                          # Django后端项目
│   ├── config/                       # 项目配置
│   │   ├── settings/
│   │   │   ├── base.py              # 基础配置
│   │   │   ├── development.py       # 开发环境
│   │   │   └── production.py        # 生产环境
│   │   ├── urls.py                  # 根URL配置
│   │   └── wsgi.py
│   │
│   ├── apps/
│   │   ├── movies/                  # 电影应用
│   │   │   ├── models.py           # 电影、演员、导演、类型模型
│   │   │   ├── serializers.py      # DRF序列化器
│   │   │   ├── views.py            # API视图
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   │
│   │   ├── users/                   # 用户应用
│   │   │   ├── models.py           # 扩展User模型
│   │   │   ├── serializers.py
│   │   │   ├── views.py            # 注册、登录、个人资料
│   │   │   └── urls.py
│   │   │
│   │   ├── reviews/                 # 影评应用
│   │   │   ├── models.py           # 影评、评论模型
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   │
│   │   ├── ratings/                 # 评分应用
│   │   │   ├── models.py           # 评分模型
│   │   │   ├── serializers.py
│   │   │   └── views.py
│   │   │
│   │   ├── watchlists/              # 观影清单应用
│   │   │   ├── models.py           # 收藏、观影状态、片单
│   │   │   ├── serializers.py
│   │   │   └── views.py
│   │   │
│   │   └── social/                  # 社交功能
│   │       ├── models.py           # 关注、动态
│   │       ├── serializers.py
│   │       └── views.py
│   │
│   ├── media/                       # 媒体文件
│   │   ├── posters/                # 电影海报
│   │   ├── avatars/                # 用户头像
│   │   └── backdrops/              # 电影背景图
│   │
│   ├── scripts/                     # 数据导入脚本
│   │   └── import_douban_data.py   # 导入豆瓣Top250数据
│   │
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   │
│   └── manage.py
│
├── frontend/                         # Vue.js前端项目
│   ├── src/
│   │   ├── assets/                  # 静态资源
│   │   │   ├── styles/
│   │   │   │   ├── main.css
│   │   │   │   └── tailwind.css
│   │   │   └── images/
│   │   │
│   │   ├── components/              # 可复用组件
│   │   │   ├── layout/
│   │   │   │   ├── Header.vue
│   │   │   │   ├── Footer.vue
│   │   │   │   └── Sidebar.vue
│   │   │   ├── movie/
│   │   │   │   ├── MovieCard.vue    # 电影卡片
│   │   │   │   ├── MovieGrid.vue    # 瀑布流网格
│   │   │   │   ├── MovieDetail.vue
│   │   │   │   └── MovieFilters.vue # 筛选组件
│   │   │   ├── review/
│   │   │   │   ├── ReviewCard.vue
│   │   │   │   ├── ReviewForm.vue
│   │   │   │   └── CommentList.vue
│   │   │   ├── user/
│   │   │   │   ├── UserProfile.vue
│   │   │   │   ├── UserCard.vue
│   │   │   │   └── FollowButton.vue
│   │   │   └── common/
│   │   │       ├── RatingStars.vue  # 星级评分
│   │   │       ├── LoadingSpinner.vue
│   │   │       ├── Pagination.vue
│   │   │       └── SearchBar.vue
│   │   │
│   │   ├── views/                   # 页面视图
│   │   │   ├── Home.vue            # 首页
│   │   │   ├── MovieList.vue       # 电影列表（瀑布流）
│   │   │   ├── MovieDetail.vue     # 电影详情
│   │   │   ├── ReviewDetail.vue    # 影评详情
│   │   │   ├── UserProfile.vue     # 用户主页
│   │   │   ├── MyWatchlist.vue     # 我的观影清单
│   │   │   ├── MyCollections.vue   # 我的片单
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   └── NotFound.vue
│   │   │
│   │   ├── router/                  # 路由配置
│   │   │   └── index.js
│   │   │
│   │   ├── stores/                  # Pinia状态管理
│   │   │   ├── auth.js             # 认证状态
│   │   │   ├── user.js             # 用户信息
│   │   │   ├── movie.js            # 电影数据
│   │   │   └── ui.js               # UI状态（加载、提示等）
│   │   │
│   │   ├── services/                # API服务层
│   │   │   ├── api.js              # Axios配置
│   │   │   ├── auth.js             # 认证API
│   │   │   ├── movies.js           # 电影API
│   │   │   ├── reviews.js          # 影评API
│   │   │   ├── users.js            # 用户API
│   │   │   └── watchlists.js       # 收藏API
│   │   │
│   │   ├── utils/                   # 工具函数
│   │   │   ├── validators.js       # 表单验证
│   │   │   ├── formatters.js       # 数据格式化
│   │   │   └── constants.js        # 常量定义
│   │   │
│   │   ├── composables/             # 组合式函数
│   │   │   ├── useInfiniteScroll.js
│   │   │   ├── useLazyImage.js
│   │   │   └── useAuth.js
│   │   │
│   │   ├── App.vue
│   │   └── main.js
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── robots.txt
│   │
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── .env.example
│
├── douban_top250/                   # 现有数据（保留）
│   ├── douban_top250.json
│   ├── douban_top250.md
│   └── images/                      # 250部电影海报
│
├── docker-compose.yml               # Docker编排（可选）
├── .gitignore
└── README.md
```

---

## 💾 数据库设计

### MySQL配置说明

本项目使用MySQL 8.0+作为数据库，以下是关键配置信息：

#### 连接信息
```
主机: 10.5.80.8
端口: 3306
数据库名: moviedb
用户名: root
密码: 123456
字符集: utf8mb4 (支持emoji和特殊字符)
```

#### Django配置示例
```python
# settings/base.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moviedb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '10.5.80.8',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': 600,
    }
}
```

#### 创建数据库
```sql
CREATE DATABASE IF NOT EXISTS moviedb
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

#### 安装MySQL客户端
```bash
# 方式1: mysqlclient (推荐)
pip install mysqlclient

# 方式2: PyMySQL (纯Python实现)
pip install pymysql
# 在 __init__.py 中添加:
# import pymysql
# pymysql.install_as_MySQLdb()
```

### ER图概览

```
User ──1:N── Review ──1:N── Comment
  │           │
  │         N:1
  │           │
  └─1:N─── Rating ──N:1── Movie ──N:M── Genre
  │           │              │
  └─1:N─── Watchlist ────N:1─┘
  │                          │
  └─1:N─── Collection ───N:M─┘
  │
  └─N:M─── UserFollow (自关联)
```

### 核心数据表设计

#### 1. 用户表 (users_user)
扩展Django的AbstractUser

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| username | CharField(50) | 用户名 | UNIQUE |
| email | EmailField | 邮箱 | UNIQUE |
| password | CharField(128) | 密码（加密） | - |
| avatar | ImageField | 头像 | - |
| bio | TextField | 个人简介 | - |
| location | CharField(100) | 所在地 | - |
| website | URLField | 个人网站 | - |
| date_joined | DateTimeField | 注册时间 | INDEX |
| last_login | DateTimeField | 最后登录 | - |
| is_active | BooleanField | 是否激活 | - |
| follower_count | IntegerField | 粉丝数 | - |
| following_count | IntegerField | 关注数 | - |

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'users_user'
        indexes = [
            models.Index(fields=['date_joined']),
        ]
```

#### 2. 电影表 (movies_movie)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| rank | IntegerField | 豆瓣排名 | INDEX |
| title | CharField(255) | 电影名称 | INDEX |
| original_title | CharField(255) | 原始标题 | - |
| year | IntegerField | 上映年份 | INDEX |
| country | CharField(100) | 国家/地区 | - |
| director | CharField(255) | 导演 | - |
| cast | TextField | 主演（逗号分隔） | - |
| genres | CharField(100) | 类型（逗号分隔） | - |
| runtime | IntegerField | 时长（分钟） | - |
| summary | TextField | 剧情简介 | - |
| poster | ImageField | 海报图片 | - |
| backdrop | ImageField | 背景图片 | - |
| douban_url | URLField | 豆瓣链接 | - |
| douban_rating | DecimalField(3,1) | 豆瓣评分 | INDEX |
| avg_rating | DecimalField(3,1) | 本站平均评分 | INDEX |
| rating_count | IntegerField | 本站评分人数 | - |
| review_count | IntegerField | 影评数量 | - |
| created_at | DateTimeField | 创建时间 | INDEX |
| updated_at | DateTimeField | 更新时间 | - |

```python
class Movie(models.Model):
    rank = models.IntegerField(db_index=True, null=True)
    title = models.CharField(max_length=255, db_index=True)
    original_title = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(db_index=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=255, blank=True)
    cast = models.TextField(blank=True)
    genres = models.CharField(max_length=100, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    summary = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/')
    backdrop = models.ImageField(upload_to='backdrops/', null=True, blank=True)
    douban_url = models.URLField(blank=True)
    douban_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    rating_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'movies_movie'
        ordering = ['rank']
        indexes = [
            models.Index(fields=['douban_rating']),
            models.Index(fields=['avg_rating']),
            models.Index(fields=['-created_at']),
        ]
```

#### 3. 类型表 (movies_genre)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | AutoField | 主键 | PK |
| name | CharField(50) | 类型名称 | UNIQUE |
| slug | SlugField(50) | URL友好名称 | UNIQUE |

```python
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'movies_genre'
```

#### 4. 电影类型关联表 (movies_moviegenre)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | AutoField | 主键 | PK |
| movie_id | ForeignKey | 电影ID | INDEX |
| genre_id | ForeignKey | 类型ID | INDEX |

#### 5. 影评表 (reviews_review)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| user_id | ForeignKey | 用户ID | INDEX |
| movie_id | ForeignKey | 电影ID | INDEX |
| title | CharField(255) | 影评标题 | - |
| content | TextField | 影评内容 | - |
| contains_spoilers | BooleanField | 包含剧透 | - |
| helpful_count | IntegerField | 有用数 | - |
| comment_count | IntegerField | 评论数 | - |
| created_at | DateTimeField | 发布时间 | INDEX |
| updated_at | DateTimeField | 更新时间 | - |

```python
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    content = models.TextField()
    contains_spoilers = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews_review'
        ordering = ['-created_at']
        unique_together = ['user', 'movie']  # 每个用户对每部电影只能写一篇影评
        indexes = [
            models.Index(fields=['movie', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
```

#### 6. 评论表 (reviews_comment)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| user_id | ForeignKey | 用户ID | INDEX |
| review_id | ForeignKey | 影评ID | INDEX |
| parent_id | ForeignKey | 父评论ID（回复） | INDEX |
| content | TextField | 评论内容 | - |
| created_at | DateTimeField | 发布时间 | INDEX |
| updated_at | DateTimeField | 更新时间 | - |

```python
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews_comment'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['review', 'created_at']),
        ]
```

#### 7. 评分表 (ratings_rating)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| user_id | ForeignKey | 用户ID | INDEX |
| movie_id | ForeignKey | 电影ID | INDEX |
| score | DecimalField(2,1) | 评分（0.5-5.0） | INDEX |
| created_at | DateTimeField | 评分时间 | INDEX |
| updated_at | DateTimeField | 更新时间 | - |

```python
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.DecimalField(max_digits=2, decimal_places=1)  # 0.5 - 5.0
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ratings_rating'
        unique_together = ['user', 'movie']
        indexes = [
            models.Index(fields=['movie', 'score']),
            models.Index(fields=['user', '-created_at']),
        ]
```

#### 8. 观影清单表 (watchlists_watchlist)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| user_id | ForeignKey | 用户ID | INDEX |
| movie_id | ForeignKey | 电影ID | INDEX |
| status | CharField(20) | 状态（想看/在看/已看） | INDEX |
| added_at | DateTimeField | 添加时间 | INDEX |
| watched_at | DateTimeField | 观看时间 | - |

```python
class Watchlist(models.Model):
    STATUS_CHOICES = [
        ('want_to_watch', '想看'),
        ('watching', '在看'),
        ('watched', '已看'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_watch')
    added_at = models.DateTimeField(auto_now_add=True)
    watched_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'watchlists_watchlist'
        unique_together = ['user', 'movie']
        indexes = [
            models.Index(fields=['user', 'status', '-added_at']),
        ]
```

#### 9. 片单表 (watchlists_collection)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| user_id | ForeignKey | 用户ID | INDEX |
| name | CharField(100) | 片单名称 | - |
| description | TextField | 片单描述 | - |
| is_public | BooleanField | 是否公开 | - |
| created_at | DateTimeField | 创建时间 | INDEX |
| updated_at | DateTimeField | 更新时间 | - |

```python
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    movies = models.ManyToManyField(Movie, through='CollectionMovie')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'watchlists_collection'
        ordering = ['-created_at']
```

#### 10. 片单电影关联表 (watchlists_collectionmovie)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| collection_id | ForeignKey | 片单ID | INDEX |
| movie_id | ForeignKey | 电影ID | INDEX |
| order | IntegerField | 排序 | - |
| added_at | DateTimeField | 添加时间 | - |

#### 11. 用户关注表 (social_userfollow)

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | BigAutoField | 主键 | PK |
| follower_id | ForeignKey | 关注者ID | INDEX |
| following_id | ForeignKey | 被关注者ID | INDEX |
| created_at | DateTimeField | 关注时间 | INDEX |

```python
class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'social_userfollow'
        unique_together = ['follower', 'following']
        indexes = [
            models.Index(fields=['follower', '-created_at']),
            models.Index(fields=['following', '-created_at']),
        ]
```

### 数据库优化策略

#### 索引优化
```sql
-- 复合索引示例
CREATE INDEX idx_review_movie_created ON reviews_review(movie_id, created_at DESC);
CREATE INDEX idx_rating_movie_score ON ratings_rating(movie_id, score DESC);
CREATE INDEX idx_watchlist_user_status ON watchlists_watchlist(user_id, status, added_at DESC);
```

#### 查询优化
```python
# 使用 select_related 优化 ForeignKey 查询（减少数据库查询次数）
reviews = Review.objects.select_related('user', 'movie').all()

# 使用 prefetch_related 优化 ManyToMany 查询
movies = Movie.objects.prefetch_related('genres').all()

# 使用 only() 只查询需要的字段
movies = Movie.objects.only('id', 'title', 'poster', 'avg_rating')

# 使用 annotate() 在数据库层面聚合
from django.db.models import Count, Avg
movies = Movie.objects.annotate(
    review_count=Count('reviews'),
    avg_rating=Avg('ratings__score')
)
```

---

## 🎨 UI/UX设计

### 设计理念
- **深色主题**：以深色背景为主，减少眼睛疲劳，突出电影海报
- **卡片瀑布流**：Pinterest风格，动态高度，充分利用屏幕空间
- **极简设计**：去除冗余元素，突出内容本身
- **响应式**：移动端优先，适配各种设备

### 配色方案

```css
/* 主色调 - 深色主题 */
--color-bg-primary: #0F1419;        /* 主背景 - 深黑蓝 */
--color-bg-secondary: #1A1D29;      /* 次级背景 - 深灰蓝 */
--color-bg-tertiary: #252A35;       /* 卡片背景 - 中灰蓝 */

/* 文字颜色 */
--color-text-primary: #FFFFFF;      /* 主要文字 - 纯白 */
--color-text-secondary: #9CA3AF;    /* 次要文字 - 灰色 */
--color-text-tertiary: #6B7280;     /* 辅助文字 - 深灰 */

/* 强调色 */
--color-accent-primary: #FFB800;    /* 主强调色 - 金黄（评分星星） */
--color-accent-secondary: #E50914;  /* 次强调色 - 红色（按钮、徽章） */
--color-accent-tertiary: #3B82F6;   /* 第三强调色 - 蓝色（链接） */

/* 状态颜色 */
--color-success: #10B981;           /* 成功 - 绿色 */
--color-warning: #F59E0B;           /* 警告 - 橙色 */
--color-error: #EF4444;             /* 错误 - 红色 */
--color-info: #3B82F6;              /* 信息 - 蓝色 */

/* 边框和分割线 */
--color-border: #374151;            /* 边框颜色 */
--color-divider: #1F2937;           /* 分割线颜色 */

/* 渐变 */
--gradient-overlay: linear-gradient(180deg, rgba(15,20,25,0) 0%, rgba(15,20,25,0.9) 100%);
--gradient-card-hover: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### 页面布局

#### 1. 首页（Home）
```
┌─────────────────────────────────────────────────────────┐
│  Header: Logo | 搜索框 | 登录/用户头像                      │
├─────────────────────────────────────────────────────────┤
│  Hero Section: 精选电影轮播（全屏背景 + 渐变遮罩）           │
│  ┌──────────────────────────────────────────────────┐   │
│  │ [肖申克的救赎背景图]                                │   │
│  │                                                  │   │
│  │  肖申克的救赎                                      │   │
│  │  ★★★★★ 9.7                                      │   │
│  │  [观看预告片] [查看详情]                            │   │
│  └──────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  Section: 高分电影 (评分 > 9.0)                          │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                   │
│  │海报│ │海报│ │海报│ │海报│ │海报│ ...                │
│  └────┘ └────┘ └────┘ └────┘ └────┘                   │
├─────────────────────────────────────────────────────────┤
│  Section: 最新影评                                       │
│  [影评卡片列表]                                          │
├─────────────────────────────────────────────────────────┤
│  Footer: 关于 | GitHub | Powered by TMDB              │
└─────────────────────────────────────────────────────────┘
```

#### 2. 电影列表页（MovieList - 瀑布流）
```
┌─────────────────────────────────────────────────────────┐
│  Header                                                 │
├─────────────────────────────────────────────────────────┤
│  筛选栏                                                  │
│  类型: [全部▼] 年代: [全部▼] 评分: [全部▼] 排序: [评分▼] │
├──────────┬──────────────────────────────────────────────┤
│          │  瀑布流卡片                                   │
│ 侧边栏   │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   │
│          │  │ 海报 │  │ 海报 │  │ 海报 │  │ 海报 │   │
│ - 剧情   │  │ 标题 │  │ 标题 │  │ 标题 │  │ 标题 │   │
│ - 喜剧   │  │ ★9.7 │  │ ★9.5 │  │ ★9.3 │  │ ★9.2 │   │
│ - 动作   │  └──────┘  └──────┘  └──────┘  └──────┘   │
│ - 爱情   │                                             │
│ ...      │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   │
│          │  │ 海报 │  │ 海报 │  │ 海报 │  │ 海报 │   │
│          │  │ 标题 │  │ 标题 │  │ 标题 │  │ 标题 │   │
│          │  │ ★9.1 │  │ ★9.0 │  │ ★8.9 │  │ ★8.8 │   │
│          │  └──────┘  └──────┘  └──────┘  └──────┘   │
│          │                                             │
│          │  [无限滚动加载更多...]                        │
└──────────┴──────────────────────────────────────────────┘
```

#### 3. 电影详情页（MovieDetail）
```
┌─────────────────────────────────────────────────────────┐
│  Header                                                 │
├─────────────────────────────────────────────────────────┤
│  Hero Section: [电影背景图 + 渐变遮罩]                     │
│  ┌────────┐                                             │
│  │        │  肖申克的救赎 (1994)                         │
│  │  海报  │  The Shawshank Redemption                   │
│  │        │  ★★★★★ 9.7 (豆瓣) | ★★★★★ 9.5 (本站)     │
│  │        │  导演: 弗兰克·德拉邦特                        │
│  └────────┘  主演: 蒂姆·罗宾斯 / 摩根·弗里曼             │
│              类型: 剧情 / 犯罪  |  时长: 142分钟          │
│              [💖 加入片单] [⭐ 评分] [✍️ 写影评]          │
├─────────────────────────────────────────────────────────┤
│  剧情简介                                                │
│  一场谋杀案使银行家安迪蒙冤入狱...                         │
├─────────────────────────────────────────────────────────┤
│  热门影评 (123)                          [查看全部 →]    │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 👤 用户A  ★★★★★  2024-01-15                       │  │
│  │ 《肖申克的救赎》：希望的力量                           │  │
│  │ 这是一部关于希望和自由的电影...                        │  │
│  │ 👍 1234 有用  💬 56 评论                            │  │
│  └───────────────────────────────────────────────────┘  │
│  [更多影评...]                                           │
├─────────────────────────────────────────────────────────┤
│  相关推荐                                                │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐                         │
│  │海报│ │海报│ │海报│ │海报│                          │
│  └────┘ └────┘ └────┘ └────┘                         │
└─────────────────────────────────────────────────────────┘
```

### 组件设计

#### MovieCard（电影卡片）
```html
<div class="movie-card">
  <div class="card-image">
    <img src="poster.jpg" loading="lazy" alt="电影标题">
    <div class="overlay">
      <button class="btn-favorite">💖</button>
      <button class="btn-rating">⭐</button>
    </div>
  </div>
  <div class="card-content">
    <h3 class="title">肖申克的救赎</h3>
    <div class="meta">
      <span class="year">1994</span>
      <span class="genre">剧情</span>
    </div>
    <div class="rating">
      <span class="stars">★★★★★</span>
      <span class="score">9.7</span>
    </div>
  </div>
</div>
```

**样式特点：**
- 悬停时缩放 1.05 倍
- 海报加载使用懒加载（Intersection Observer）
- 遮罩层使用渐变半透明背景
- 卡片阴影：`box-shadow: 0 4px 6px rgba(0,0,0,0.3)`
- 圆角：`border-radius: 12px`

#### RatingStars（星级评分）
```html
<div class="rating-stars">
  <span class="star filled">★</span>
  <span class="star filled">★</span>
  <span class="star filled">★</span>
  <span class="star half">★</span>
  <span class="star empty">☆</span>
  <span class="score">3.5</span>
</div>
```

### 响应式断点

```css
/* 移动端 */
@media (max-width: 640px) {
  .movie-grid {
    grid-template-columns: repeat(2, 1fr); /* 2列 */
    gap: 12px;
  }
}

/* 平板 */
@media (min-width: 641px) and (max-width: 1024px) {
  .movie-grid {
    grid-template-columns: repeat(3, 1fr); /* 3列 */
    gap: 16px;
  }
}

/* 桌面 */
@media (min-width: 1025px) and (max-width: 1440px) {
  .movie-grid {
    grid-template-columns: repeat(4, 1fr); /* 4列 */
    gap: 20px;
  }
}

/* 大屏 */
@media (min-width: 1441px) {
  .movie-grid {
    grid-template-columns: repeat(5, 1fr); /* 5列 */
    gap: 24px;
  }
}
```

### 瀑布流实现方案

#### 方案1：CSS Grid（推荐）
```css
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-auto-rows: 10px;  /* 小行高，实现瀑布流效果 */
  gap: 20px;
}

.movie-card {
  grid-row-end: span 40;  /* 根据内容动态调整 */
}
```

#### 方案2：Vue组件库（更简单）
```vue
<template>
  <masonry-wall :items="movies" :column-width="250" :gap="20">
    <template #default="{ item }">
      <MovieCard :movie="item" />
    </template>
  </masonry-wall>
</template>

<script setup>
import MasonryWall from 'vue-masonry-wall';
</script>
```

---

## 🔌 API接口设计

### RESTful API规范

#### 基础URL
```
开发环境: http://localhost:8000/api/v1/
生产环境: https://yourdomain.com/api/v1/
```

#### 认证方式
```
Authorization: Bearer <access_token>
```

### 核心API接口列表

#### 1. 认证接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | /auth/register/ | 用户注册 | ❌ |
| POST | /auth/login/ | 用户登录 | ❌ |
| POST | /auth/logout/ | 用户登出 | ✅ |
| POST | /auth/refresh/ | 刷新Token | ❌ |
| GET | /auth/me/ | 获取当前用户信息 | ✅ |
| PUT | /auth/me/ | 更新个人资料 | ✅ |
| POST | /auth/change-password/ | 修改密码 | ✅ |

**示例：注册**
```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "username": "moviefan",
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}

Response 201:
{
  "id": 1,
  "username": "moviefan",
  "email": "user@example.com",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**示例：登录**
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "moviefan",
  "password": "securepassword123"
}

Response 200:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "moviefan",
    "email": "user@example.com",
    "avatar": "/media/avatars/default.jpg"
  }
}
```

#### 2. 电影接口

| 方法 | 端点 | 说明 | 认证 | 参数 |
|------|------|------|------|------|
| GET | /movies/ | 电影列表 | ❌ | page, page_size, genre, year, rating_gte, ordering |
| GET | /movies/{id}/ | 电影详情 | ❌ | - |
| GET | /movies/top-rated/ | 高分电影 | ❌ | limit |
| GET | /movies/search/ | 搜索电影 | ❌ | q, page |
| GET | /movies/{id}/reviews/ | 电影影评列表 | ❌ | page |
| GET | /movies/{id}/similar/ | 相似电影推荐 | ❌ | limit |

**示例：电影列表（带筛选）**
```http
GET /api/v1/movies/?genre=剧情&year=1994&rating_gte=9.0&ordering=-avg_rating&page=1&page_size=20

Response 200:
{
  "count": 50,
  "next": "/api/v1/movies/?page=2&...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "rank": 1,
      "title": "肖申克的救赎",
      "year": 1994,
      "genres": ["剧情", "犯罪"],
      "director": "弗兰克·德拉邦特",
      "cast": ["蒂姆·罗宾斯", "摩根·弗里曼"],
      "poster": "/media/posters/001_肖申克的救赎.jpg",
      "douban_rating": 9.7,
      "avg_rating": 9.5,
      "rating_count": 1234,
      "review_count": 89
    },
    ...
  ]
}
```

**示例：电影详情**
```http
GET /api/v1/movies/1/

Response 200:
{
  "id": 1,
  "rank": 1,
  "title": "肖申克的救赎",
  "original_title": "The Shawshank Redemption",
  "year": 1994,
  "country": "美国",
  "genres": ["剧情", "犯罪"],
  "director": "弗兰克·德拉邦特",
  "cast": ["蒂姆·罗宾斯", "摩根·弗里曼"],
  "runtime": 142,
  "summary": "一场谋杀案使银行家安迪蒙冤入狱...",
  "poster": "/media/posters/001_肖申克的救赎.jpg",
  "backdrop": "/media/backdrops/001_肖申克的救赎.jpg",
  "douban_url": "https://movie.douban.com/subject/1292052/",
  "douban_rating": 9.7,
  "avg_rating": 9.5,
  "rating_count": 1234,
  "review_count": 89,
  "user_rating": 5.0,  // 当前用户评分（需认证）
  "user_watchlist_status": "watched",  // 用户观影状态（需认证）
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 3. 影评接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | /reviews/ | 影评列表 | ❌ |
| POST | /reviews/ | 创建影评 | ✅ |
| GET | /reviews/{id}/ | 影评详情 | ❌ |
| PUT | /reviews/{id}/ | 更新影评 | ✅ |
| DELETE | /reviews/{id}/ | 删除影评 | ✅ |
| POST | /reviews/{id}/helpful/ | 标记有用 | ✅ |
| GET | /reviews/{id}/comments/ | 影评评论列表 | ❌ |
| POST | /reviews/{id}/comments/ | 发表评论 | ✅ |

**示例：创建影评**
```http
POST /api/v1/reviews/
Authorization: Bearer <token>
Content-Type: application/json

{
  "movie": 1,
  "title": "希望的力量",
  "content": "这是一部关于希望和自由的电影...",
  "contains_spoilers": false
}

Response 201:
{
  "id": 123,
  "user": {
    "id": 1,
    "username": "moviefan",
    "avatar": "/media/avatars/user1.jpg"
  },
  "movie": {
    "id": 1,
    "title": "肖申克的救赎",
    "poster": "/media/posters/001_肖申克的救赎.jpg"
  },
  "title": "希望的力量",
  "content": "这是一部关于希望和自由的电影...",
  "contains_spoilers": false,
  "helpful_count": 0,
  "comment_count": 0,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### 4. 评分接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | /ratings/ | 评分/更新评分 | ✅ |
| DELETE | /ratings/{movie_id}/ | 删除评分 | ✅ |
| GET | /users/{user_id}/ratings/ | 用户评分列表 | ❌ |

**示例：评分**
```http
POST /api/v1/ratings/
Authorization: Bearer <token>
Content-Type: application/json

{
  "movie": 1,
  "score": 5.0
}

Response 201:
{
  "id": 456,
  "movie": 1,
  "score": 5.0,
  "created_at": "2024-01-15T10:35:00Z"
}
```

#### 5. 观影清单接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | /watchlist/ | 我的观影清单 | ✅ |
| POST | /watchlist/ | 添加到观影清单 | ✅ |
| PUT | /watchlist/{movie_id}/ | 更新观影状态 | ✅ |
| DELETE | /watchlist/{movie_id}/ | 从观影清单移除 | ✅ |

**示例：添加到观影清单**
```http
POST /api/v1/watchlist/
Authorization: Bearer <token>
Content-Type: application/json

{
  "movie": 1,
  "status": "want_to_watch"
}

Response 201:
{
  "id": 789,
  "movie": {
    "id": 1,
    "title": "肖申克的救赎",
    "poster": "/media/posters/001_肖申克的救赎.jpg"
  },
  "status": "want_to_watch",
  "added_at": "2024-01-15T10:40:00Z"
}
```

#### 6. 片单接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | /collections/ | 片单列表 | ❌ |
| POST | /collections/ | 创建片单 | ✅ |
| GET | /collections/{id}/ | 片单详情 | ❌ |
| PUT | /collections/{id}/ | 更新片单 | ✅ |
| DELETE | /collections/{id}/ | 删除片单 | ✅ |
| POST | /collections/{id}/add-movie/ | 添加电影到片单 | ✅ |
| DELETE | /collections/{id}/remove-movie/ | 从片单移除电影 | ✅ |

#### 7. 用户接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | /users/{id}/ | 用户资料 | ❌ |
| GET | /users/{id}/reviews/ | 用户影评列表 | ❌ |
| GET | /users/{id}/ratings/ | 用户评分列表 | ❌ |
| GET | /users/{id}/watchlist/ | 用户观影清单（公开） | ❌ |
| GET | /users/{id}/collections/ | 用户片单列表 | ❌ |
| GET | /users/{id}/followers/ | 用户粉丝列表 | ❌ |
| GET | /users/{id}/following/ | 用户关注列表 | ❌ |
| POST | /users/{id}/follow/ | 关注用户 | ✅ |
| DELETE | /users/{id}/unfollow/ | 取消关注 | ✅ |

#### 8. 社交接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | /feed/ | 动态流（关注用户的活动） | ✅ |
| GET | /notifications/ | 通知列表 | ✅ |
| PUT | /notifications/{id}/read/ | 标记通知已读 | ✅ |

### API响应格式

#### 成功响应
```json
{
  "data": { ... },
  "message": "操作成功"
}
```

#### 错误响应
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "验证失败",
    "details": {
      "email": ["该邮箱已被注册"]
    }
  }
}
```

#### 分页响应
```json
{
  "count": 250,
  "next": "/api/v1/movies/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## 🔐 安全性设计

### JWT认证机制

#### Token配置
```python
# settings.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # 访问令牌15分钟
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # 刷新令牌7天
    'ROTATE_REFRESH_TOKENS': True,                   # 刷新时轮换refresh token
    'BLACKLIST_AFTER_ROTATION': True,                # 轮换后将旧token加入黑名单
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

#### Token存储（前端）
```javascript
// 推荐方式：存储在内存 + httpOnly cookie
// 1. Access Token 存储在内存（Pinia store）
// 2. Refresh Token 存储在 httpOnly cookie（后端设置）

// stores/auth.js
export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
    user: null,
  }),

  actions: {
    async login(credentials) {
      const response = await api.post('/auth/login/', credentials);
      this.accessToken = response.data.access;
      this.user = response.data.user;
      // Refresh token 自动存储在 httpOnly cookie
    },

    async refreshToken() {
      const response = await api.post('/auth/refresh/');
      this.accessToken = response.data.access;
    },
  },
});
```

### CORS配置

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Vue开发服务器
    "http://127.0.0.1:3000",
    "https://yourdomain.com",     # 生产环境
]

CORS_ALLOW_CREDENTIALS = True      # 允许携带cookies

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'user-agent',
]
```

### 输入验证

#### 后端验证（DRF Serializer）
```python
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={'blank': '标题不能为空'}
    )
    content = serializers.CharField(
        min_length=10,
        max_length=10000,
        error_messages={
            'min_length': '影评内容至少10个字符',
            'max_length': '影评内容不能超过10000个字符'
        }
    )

    def validate_content(self, value):
        # XSS防护：过滤HTML标签
        from bleach import clean
        return clean(value, tags=[], strip=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'contains_spoilers']
```

#### 前端验证
```javascript
// utils/validators.js
export const validators = {
  required: (value) => !!value || '该字段不能为空',

  email: (value) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(value) || '邮箱格式不正确';
  },

  minLength: (min) => (value) =>
    value.length >= min || `至少需要${min}个字符`,

  maxLength: (max) => (value) =>
    value.length <= max || `不能超过${max}个字符`,

  password: (value) => {
    if (value.length < 8) return '密码至少8个字符';
    if (!/[A-Z]/.test(value)) return '密码必须包含大写字母';
    if (!/[a-z]/.test(value)) return '密码必须包含小写字母';
    if (!/[0-9]/.test(value)) return '密码必须包含数字';
    return true;
  },
};
```

### 速率限制

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',      # 匿名用户：100次/小时
        'user': '1000/hour',     # 认证用户：1000次/小时
        'login': '5/hour',       # 登录接口：5次/小时
    }
}

# views.py
from rest_framework.throttling import UserRateThrottle

class LoginThrottle(UserRateThrottle):
    rate = '5/hour'

class LoginView(APIView):
    throttle_classes = [LoginThrottle]
    # ...
```

### 其他安全措施

```python
# settings.py - 生产环境
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')  # 从环境变量读取
ALLOWED_HOSTS = ['yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 其他安全头
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# CSP (Content Security Policy)
CSP_DEFAULT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:", "https://img3.doubanio.com")
CSP_SCRIPT_SRC = ("'self'",)
```

---

## ⚡ 性能优化

### 前端性能优化

#### 1. 图片懒加载
```vue
<!-- components/movie/MovieCard.vue -->
<template>
  <div class="movie-card">
    <img
      :data-src="movie.poster"
      :alt="movie.title"
      class="lazy-image"
      ref="imageRef"
    >
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps(['movie']);
const imageRef = ref(null);

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.add('loaded');
        observer.unobserve(img);
      }
    });
  });

  if (imageRef.value) {
    observer.observe(imageRef.value);
  }
});
</script>
```

#### 2. 无限滚动
```javascript
// composables/useInfiniteScroll.js
import { ref, onMounted, onUnmounted } from 'vue';

export function useInfiniteScroll(callback) {
  const isLoading = ref(false);
  const hasMore = ref(true);

  const handleScroll = () => {
    const scrollTop = window.pageYOffset;
    const scrollHeight = document.documentElement.scrollHeight;
    const clientHeight = window.innerHeight;

    // 距离底部 200px 时触发加载
    if (scrollTop + clientHeight >= scrollHeight - 200) {
      if (!isLoading.value && hasMore.value) {
        isLoading.value = true;
        callback().finally(() => {
          isLoading.value = false;
        });
      }
    }
  };

  onMounted(() => {
    window.addEventListener('scroll', handleScroll);
  });

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
  });

  return { isLoading, hasMore };
}

// 使用
const { isLoading, hasMore } = useInfiniteScroll(async () => {
  const newMovies = await fetchMoreMovies();
  movies.value.push(...newMovies);
  if (newMovies.length === 0) hasMore.value = false;
});
```

#### 3. 代码分割
```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),  // 懒加载
  },
  {
    path: '/movies',
    name: 'MovieList',
    component: () => import('@/views/MovieList.vue'),
  },
  {
    path: '/movies/:id',
    name: 'MovieDetail',
    component: () => import('@/views/MovieDetail.vue'),
  },
];
```

#### 4. 缓存策略
```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// 简单的内存缓存
const cache = new Map();
const CACHE_DURATION = 5 * 60 * 1000;  // 5分钟

api.interceptors.request.use((config) => {
  if (config.method === 'get' && config.cache) {
    const cacheKey = config.url + JSON.stringify(config.params);
    const cached = cache.get(cacheKey);

    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
      config.adapter = () => Promise.resolve({
        data: cached.data,
        status: 200,
        statusText: 'OK (cached)',
        config,
      });
    }
  }
  return config;
});

api.interceptors.response.use((response) => {
  if (response.config.cache) {
    const cacheKey = response.config.url + JSON.stringify(response.config.params);
    cache.set(cacheKey, {
      data: response.data,
      timestamp: Date.now(),
    });
  }
  return response;
});
```

### 后端性能优化

#### 1. 数据库查询优化
```python
# views.py
from rest_framework import viewsets
from django.db.models import Count, Avg, Prefetch

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset = Movie.objects.select_related(
            # 优化外键查询
        ).prefetch_related(
            'genres',  # 优化多对多查询
            Prefetch(
                'reviews',
                queryset=Review.objects.select_related('user').order_by('-created_at')[:5]
            )
        ).annotate(
            # 在数据库层面计算聚合数据
            review_count=Count('reviews'),
            avg_rating=Avg('ratings__score')
        )

        # 只查询需要的字段
        if self.action == 'list':
            queryset = queryset.only(
                'id', 'rank', 'title', 'year', 'poster',
                'douban_rating', 'avg_rating'
            )

        return queryset
```

#### 2. Redis缓存
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# views.py
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    # 缓存电影列表 15分钟
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        movie_id = kwargs.get('pk')
        cache_key = f'movie_{movie_id}'

        # 尝试从缓存获取
        movie = cache.get(cache_key)
        if not movie:
            movie = self.get_object()
            # 缓存1小时
            cache.set(cache_key, movie, 60 * 60)

        serializer = self.get_serializer(movie)
        return Response(serializer.data)
```

#### 3. 数据库连接池
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moviedb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '10.5.80.8',
        'PORT': '3306',
        'CONN_MAX_AGE': 600,  # 连接池：保持连接10分钟
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

#### 4. 分页优化
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# pagination.py
from rest_framework.pagination import CursorPagination

class MovieCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'  # 游标分页，性能更好
```

### 图片优化

```python
# models.py
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Movie(models.Model):
    poster = models.ImageField(upload_to='posters/')

    def save(self, *args, **kwargs):
        if self.poster:
            # 压缩图片
            img = Image.open(self.poster)

            # 转换为RGB（如果是RGBA）
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background

            # 调整尺寸（宽度最大500px）
            max_width = 500
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (max_width, int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)

            # 保存为JPEG，质量85
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)

            self.poster = InMemoryUploadedFile(
                output, 'ImageField',
                f"{self.poster.name.split('.')[0]}.jpg",
                'image/jpeg', output.getbuffer().nbytes, None
            )

        super().save(*args, **kwargs)
```

---

## 📊 实施计划

### 第一阶段：MVP（最小可行产品）- 3-4周

**目标：** 基础功能上线，用户可以浏览电影、注册、评分

#### Week 1: 项目搭建 + 后端基础
- [ ] 初始化Django项目和Vue项目
- [ ] 配置数据库（MySQL: 10.5.80.8:3306）和Redis
- [ ] 创建数据库模型（User, Movie, Rating, Review）
- [ ] 编写数据导入脚本，导入豆瓣Top250数据
- [ ] 配置Django REST Framework
- [ ] 实现JWT认证（注册、登录、登出）

#### Week 2: 核心API开发
- [ ] 实现电影API（列表、详情、搜索）
- [ ] 实现评分API（创建、更新、删除）
- [ ] 实现影评API（创建、列表、详情）
- [ ] 实现用户API（个人资料、更新）
- [ ] 编写API文档（drf-spectacular）
- [ ] API测试

#### Week 3: 前端核心功能
- [ ] 搭建Vue项目结构
- [ ] 配置Tailwind CSS和路由
- [ ] 实现认证页面（登录、注册）
- [ ] 实现首页（精选电影展示）
- [ ] 实现电影列表页（瀑布流布局）
- [ ] 实现电影详情页
- [ ] 实现评分功能

#### Week 4: 前端完善 + 测试
- [ ] 实现影评功能（查看、发布）
- [ ] 实现搜索和筛选功能
- [ ] 实现个人中心基础页面
- [ ] 响应式设计优化
- [ ] 前后端联调
- [ ] 功能测试和bug修复
- [ ] MVP版本部署

### 第二阶段：核心功能完善 - 3-4周

**目标：** 完善用户体验，增加社交功能

#### Week 5-6: 观影清单和片单
- [ ] 实现观影清单功能（想看/在看/已看）
- [ ] 实现自定义片单功能
- [ ] 片单分享功能
- [ ] 个人中心完善（影评列表、评分历史、片单管理）

#### Week 7-8: 社交功能
- [ ] 实现用户关注功能
- [ ] 实现动态流（关注用户的活动）
- [ ] 实现评论功能（影评下的评论）
- [ ] 实现通知系统
- [ ] 用户主页完善

### 第三阶段：增强功能 - 2-3周

**目标：** 增加高级功能，提升用户留存

#### Week 9-10: 推荐和搜索优化
- [ ] 实现基于协同过滤的推荐算法
- [ ] 优化搜索功能（全文搜索）
- [ ] 实现相似电影推荐
- [ ] 实现高级筛选（多条件组合）
- [ ] 热门影评、热门电影榜单

#### Week 11: 内容管理
- [ ] 完善Django Admin后台
- [ ] 实现内容审核功能（可选）
- [ ] 数据统计和分析
- [ ] 导出功能（用户数据导出）

### 第四阶段：优化和上线 - 2周

**目标：** 性能优化，准备生产环境

#### Week 12-13: 性能优化
- [ ] 数据库查询优化
- [ ] Redis缓存配置
- [ ] 图片CDN配置
- [ ] 前端性能优化（懒加载、代码分割）
- [ ] SEO优化（meta标签、sitemap）
- [ ] 安全性检查

#### Week 14: 部署和上线
- [ ] 配置生产环境（Nginx, Gunicorn）
- [ ] 配置HTTPS（Let's Encrypt）
- [ ] 配置域名和DNS
- [ ] 数据库备份策略
- [ ] 监控和日志配置
- [ ] 正式上线

---

## 🚀 部署方案

### 开发环境

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# 前端
cd frontend
npm install
npm run dev
```

### 生产环境架构

```
用户 → Cloudflare CDN
    → Nginx (反向代理)
        → Vue.js静态文件 (前端)
        → Gunicorn + Django (后端API)
            → MySQL (数据库: 10.5.80.8:3306)
            → Redis (缓存 + 会话)
```

### Docker部署（推荐）

```yaml
# docker-compose.yml
version: '3.8'

services:
  # 注意: 数据库使用外部MySQL服务器 (10.5.80.8:3306)
  # 如需本地MySQL容器，取消下面注释
  # db:
  #   image: mysql:8.0
  #   volumes:
  #     - mysql_data:/var/lib/mysql
  #   environment:
  #     - MYSQL_DATABASE=moviedb
  #     - MYSQL_ROOT_PASSWORD=123456
  #   ports:
  #     - "3306:3306"
  #   command: --default-authentication-plugin=mysql_native_password

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/app
      - media_files:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - DEBUG=False
      - DB_ENGINE=django.db.backends.mysql
      - DB_NAME=moviedb
      - DB_USER=root
      - DB_PASSWORD=123456
      - DB_HOST=10.5.80.8
      - DB_PORT=3306
      - REDIS_URL=redis://redis:6379/0

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - media_files:/media
      - certbot_certs:/etc/letsencrypt
    depends_on:
      - backend
      - frontend

volumes:
  # postgres_data:  # 不再需要，使用外部MySQL
  media_files:
  certbot_certs:
```

---

## 📝 附加说明

### 环境变量配置

```bash
# backend/.env.example
DEBUG=True
SECRET_KEY=your-secret-key-here

# MySQL数据库配置
DB_ENGINE=django.db.backends.mysql
DB_NAME=moviedb
DB_USER=root
DB_PASSWORD=123456
DB_HOST=10.5.80.8
DB_PORT=3306

# Redis配置
REDIS_URL=redis://localhost:6379/0

# 其他配置
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Email配置（可选）
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

```bash
# frontend/.env.example
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=电影博客
VITE_APP_DESCRIPTION=基于豆瓣Top250的电影社区
```

### 数据导入脚本示例

```python
# backend/scripts/import_douban_data.py
import json
import os
from django.core.files import File
from apps.movies.models import Movie

def import_movies():
    # 读取JSON数据
    json_path = '../../douban_top250/douban_top250.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        movies_data = json.load(f)

    for item in movies_data:
        # 解析电影信息
        title = item['title'].split('/')[0].strip()
        info_parts = item['info'].split('\xa0/\xa0')

        # 提取导演、演员等信息
        director = ''
        cast = ''
        year = None
        country = ''
        genres = ''

        for part in info_parts:
            if '导演:' in part:
                director = part.replace('导演:', '').strip()
            elif '主演:' in part:
                cast = part.replace('主演:', '').strip()
            elif part.isdigit() and len(part) == 4:
                year = int(part)
            elif '/' in part:
                genres = part.strip()
            else:
                country = part.strip()

        # 创建或更新电影
        movie, created = Movie.objects.update_or_create(
            rank=int(item['rank']),
            defaults={
                'title': title,
                'original_title': item['title'],
                'year': year,
                'country': country,
                'director': director,
                'cast': cast,
                'genres': genres,
                'summary': item['summary'],
                'douban_url': item['detail_url'],
                'douban_rating': float(item['rating']),
            }
        )

        # 复制海报图片
        if item['local_image']:
            image_path = f"../../douban_top250/images/{item['local_image']}"
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    movie.poster.save(
                        item['local_image'],
                        File(img_file),
                        save=True
                    )

        print(f"{'Created' if created else 'Updated'}: {title}")

if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    django.setup()
    import_movies()
```

### 推荐的Python包

```
# requirements/base.txt
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.0
django-filter==23.3
drf-spectacular==0.26.5
mysqlclient==2.2.0           # MySQL数据库驱动
redis==5.0.1
django-redis==5.4.0
celery==5.3.4
Pillow==10.1.0
bleach==6.1.0
python-dotenv==1.0.0

# requirements/development.txt
-r base.txt
django-debug-toolbar==4.2.0
ipython==8.17.2
black==23.11.0
isort==5.12.0

# requirements/production.txt
-r base.txt
gunicorn==21.2.0
whitenoise==6.6.0
sentry-sdk==1.38.0
```

### 推荐的npm包

```json
// frontend/package.json
{
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2",
    "tailwindcss": "^3.3.5",
    "flowbite": "^2.1.1",
    "flowbite-vue": "^0.1.1",
    "vue-masonry-wall": "^2.0.5",
    "@headlessui/vue": "^1.7.16"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.2",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "eslint": "^8.54.0",
    "prettier": "^3.1.0"
  }
}
```

---

## 📚 参考资源

### 学习资源
- **Django官方文档**: https://docs.djangoproject.com/
- **DRF官方文档**: https://www.django-rest-framework.org/
- **Vue.js官方文档**: https://vuejs.org/
- **Tailwind CSS**: https://tailwindcss.com/
- **MySQL文档**: https://dev.mysql.com/doc/

### 设计灵感
- **豆瓣电影**: https://movie.douban.com/
- **IMDb**: https://www.imdb.com/
- **Letterboxd**: https://letterboxd.com/
- **The Movie Database (TMDB)**: https://www.themoviedb.org/

### 开发工具
- **Postman**: API测试
- **MySQL Workbench**: MySQL管理工具
- **phpMyAdmin**: MySQL Web管理界面
- **Redis Insight**: Redis可视化
- **Vue DevTools**: Vue调试

---

## ✅ 项目检查清单

### 开发阶段
- [ ] 数据库设计完成并创建迁移文件
- [ ] 所有API接口实现并测试通过
- [ ] 前端所有页面实现
- [ ] 响应式设计适配移动端
- [ ] 表单验证（前端+后端）
- [ ] 错误处理和用户反馈
- [ ] 代码规范检查（ESLint, Black）

### 性能优化
- [ ] 数据库查询优化（N+1问题）
- [ ] Redis缓存配置
- [ ] 图片懒加载
- [ ] 代码分割和懒加载
- [ ] 图片压缩和优化
- [ ] CDN配置

### 安全检查
- [ ] JWT认证正确实现
- [ ] CORS正确配置
- [ ] 输入验证和XSS防护
- [ ] SQL注入防护（Django ORM）
- [ ] CSRF保护
- [ ] 速率限制
- [ ] HTTPS配置

### 部署准备
- [ ] 环境变量配置
- [ ] 数据库备份策略
- [ ] 日志配置
- [ ] 监控配置（可选）
- [ ] 域名和DNS配置
- [ ] SSL证书配置
- [ ] 静态文件CDN

### 文档
- [ ] API文档（Swagger/OpenAPI）
- [ ] README.md（项目说明）
- [ ] 部署文档
- [ ] 用户使用指南（可选）

---

## 🎉 总结

本设计方案提供了一个**完整的电影博客网站**架构，具备以下特点：

### 技术特点
✅ **现代化技术栈** - Django REST + Vue.js 3 前后端分离
✅ **高性能设计** - Redis缓存、数据库优化、图片懒加载
✅ **安全可靠** - JWT认证、输入验证、速率限制
✅ **可扩展架构** - 清晰的模块划分，易于维护和扩展

### 功能特点
✅ **电影展示** - 豆瓣Top250数据，卡片瀑布流布局
✅ **用户系统** - 注册登录、个人资料、关注功能
✅ **内容创作** - 影评发布、评分、评论
✅ **个人管理** - 观影清单、自定义片单
✅ **社交互动** - 关注用户、动态流、评论互动

### 设计特点
✅ **现代化UI** - 深色主题、卡片式设计、响应式布局
✅ **优秀体验** - 流畅动画、即时反馈、无限滚动
✅ **移动友好** - 移动端优先，完美适配各种设备

---

**预计开发时间：** 10-14周（根据团队规模和经验）
**推荐团队配置：** 1-2名全栈开发者或前后端各1名

**祝开发顺利！🚀**
