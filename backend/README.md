# 电影博客后端

基于Django REST Framework的电影博客后端API。

## 技术栈

- Django 4.2
- Django REST Framework 3.14
- MySQL 8.0+
- Redis 7+
- JWT认证

## 安装步骤

### 1. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 到 `.env` 并修改配置：

```bash
cp .env.example .env
```

### 4. 数据库配置

确保MySQL数据库已经创建：

```sql
CREATE DATABASE IF NOT EXISTS moviedb
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 5. 运行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级用户

```bash
python manage.py createsuperuser
```

### 7. 导入豆瓣Top250数据

```bash
python scripts/import_douban_data.py
```

### 8. 运行开发服务器

```bash
python manage.py runserver
```

## API文档

启动服务器后访问：

- Swagger UI: http://localhost:8000/api/docs/
- API Schema: http://localhost:8000/api/schema/

## API端点

### 认证相关
- POST `/api/v1/auth/register/` - 用户注册
- POST `/api/v1/auth/login/` - 用户登录
- POST `/api/v1/auth/refresh/` - 刷新Token
- GET `/api/v1/auth/me/` - 获取当前用户信息
- PUT `/api/v1/auth/me/` - 更新个人资料

### 电影相关
- GET `/api/v1/movies/` - 电影列表
- GET `/api/v1/movies/{id}/` - 电影详情
- GET `/api/v1/movies/top_rated/` - 高分电影
- GET `/api/v1/movies/search/?q=关键词` - 搜索电影

### 影评相关
- GET `/api/v1/reviews/` - 影评列表
- POST `/api/v1/reviews/` - 创建影评
- GET `/api/v1/reviews/{id}/` - 影评详情
- PUT `/api/v1/reviews/{id}/` - 更新影评
- DELETE `/api/v1/reviews/{id}/` - 删除影评

### 评分相关
- POST `/api/v1/ratings/` - 评分/更新评分
- GET `/api/v1/ratings/` - 我的评分列表

### 观影清单
- GET `/api/v1/watchlist/` - 我的观影清单
- POST `/api/v1/watchlist/` - 添加到观影清单
- PUT `/api/v1/watchlist/{id}/` - 更新观影状态
- DELETE `/api/v1/watchlist/{id}/` - 移除

## 数据库结构

- `users_user` - 用户表
- `movies_movie` - 电影表
- `movies_genre` - 电影类型表
- `reviews_review` - 影评表
- `reviews_comment` - 评论表
- `ratings_rating` - 评分表
- `watchlists_watchlist` - 观影清单表

## 开发说明

### 运行测试

```bash
python manage.py test
```

### 创建新应用

```bash
python manage.py startapp app_name
```

### 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

## 许可证

MIT License
