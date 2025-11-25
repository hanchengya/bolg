# 基于Django + Vue.js + AI的电影推荐社区系统

**毕业设计项目总结文档**

---

## 📋 项目概述

### 1.1 项目背景

本项目是一个集成了人工智能技术的现代化电影社区平台，旨在为用户提供电影浏览、影评发布、智能推荐等功能。系统采用前后端分离架构，后端使用Django REST Framework构建RESTful API，前端使用Vue.js 3打造现代化用户界面，并集成了基于Ollama的AI聊天助手，提供智能化的电影推荐服务。

### 1.2 核心功能

- **电影展示系统**：展示豆瓣Top250电影，支持搜索、筛选和分页
- **用户系统**：注册、登录、个人资料管理，基于JWT的安全认证
- **影评系统**：发布影评、评论、互动，支持"有用"标记
- **评分系统**：用户评分，自动计算电影平均分
- **观影清单**：管理想看、在看、已看状态
- **AI聊天助手**：智能电影推荐，问答系统，基于LoRA微调的大语言模型

### 1.3 技术特色

- ✅ 前后端完全分离架构
- ✅ RESTful API设计规范
- ✅ JWT Token认证机制
- ✅ 响应式UI设计，移动端适配
- ✅ AI大模型集成与微调
- ✅ 自动化API文档生成
- ✅ 数据库查询优化
- ✅ CORS跨域解决方案

---

## 🏗️ 技术架构

### 2.1 整体架构

```
┌─────────────┐      HTTP/REST      ┌─────────────┐
│             │ ←──────────────────→ │             │
│   Vue.js    │                      │   Django    │
│   Frontend  │                      │   Backend   │
│             │                      │             │
└─────────────┘                      └──────┬──────┘
      │                                     │
      │                                     │
      ↓                                     ↓
┌─────────────┐                      ┌─────────────┐
│  Browser    │                      │    MySQL    │
│  Storage    │                      │   Database  │
└─────────────┘                      └─────────────┘
                                           ↑
                                           │
                                     ┌─────┴──────┐
                                     │   Ollama   │
                                     │  AI Model  │
                                     └────────────┘
```

### 2.2 技术栈详解

#### 后端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.12 | 编程语言 |
| Django | 4.2.7 | Web框架 |
| Django REST Framework | 3.14.0 | API框架 |
| MySQL | 8.0+ | 关系型数据库 |
| Redis | 7+ | 缓存系统 |
| JWT | 5.3.0 | Token认证 |
| drf-spectacular | 0.26.5 | API文档生成 |

#### 前端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Vue.js | 3.5.24 | 前端框架 |
| Vite | 7.2.2 | 构建工具 |
| Vue Router | 4.6.3 | 路由管理 |
| Pinia | 3.0.4 | 状态管理 |
| Tailwind CSS | 3.4.18 | CSS框架 |
| Axios | 1.13.2 | HTTP客户端 |

#### AI技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Ollama | Latest | 模型推理服务 |
| DeepSeek-7B | Chat | 基础语言模型 |
| LoRA | - | 模型微调技术 |
| Transformers | 4.x | 模型训练框架 |
| PEFT | Latest | 参数高效微调 |

---

## 📦 后端开发详解

### 3.1 项目结构

```
backend/
├── config/                    # 项目配置
│   ├── settings/
│   │   └── base.py           # 基础配置
│   ├── urls.py               # 主路由
│   └── wsgi.py
├── apps/                      # Django应用
│   ├── users/                # 用户系统
│   ├── movies/               # 电影系统
│   ├── reviews/              # 影评系统
│   ├── ratings/              # 评分系统
│   └── watchlists/           # 观影清单
├── media/                     # 媒体文件
│   └── posters/              # 电影海报
├── scripts/                   # 工具脚本
│   └── import_douban_data.py # 数据导入
├── requirements.txt           # 依赖管理
└── manage.py                 # Django命令行工具
```

### 3.2 数据库设计

#### 核心数据模型

**用户模型 (User)**
```python
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**电影模型 (Movie)**
```python
class Movie(models.Model):
    rank = models.IntegerField()           # 排名
    title = models.CharField(max_length=255)
    directors = models.TextField()
    actors = models.TextField()
    genres = models.ManyToManyField(Genre)
    rating = models.DecimalField()         # 豆瓣评分
    rating_count = models.IntegerField()   # 评分人数
    year = models.IntegerField()
    country = models.CharField(max_length=100)
    poster = models.ImageField()
    summary = models.TextField()
```

**影评模型 (Review)**
```python
class Review(models.Model):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField()         # 1-5星
    helpful_count = models.IntegerField()
    created_at = models.DateTimeField()
```

**评分模型 (Rating)**
```python
class Rating(models.Model):
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    score = models.IntegerField()          # 1-10分
    created_at = models.DateTimeField()
    
    class Meta:
        unique_together = [['user', 'movie']]
```

### 3.3 API接口设计

#### 认证接口
```
POST /api/v1/auth/register/       # 用户注册
POST /api/v1/auth/login/          # 用户登录
POST /api/v1/auth/refresh/        # 刷新Token
GET  /api/v1/auth/me/             # 获取当前用户信息
PUT  /api/v1/auth/me/             # 更新个人资料
POST /api/v1/auth/change-password/ # 修改密码
```

#### 电影接口
```
GET  /api/v1/movies/              # 电影列表（分页、筛选）
GET  /api/v1/movies/{id}/         # 电影详情
GET  /api/v1/movies/top_rated/    # 高分电影
GET  /api/v1/movies/search/       # 搜索电影
```

#### AI聊天接口
```
POST /api/movies/chat/            # AI对话
POST /api/movies/recommend/       # 电影推荐
```

### 3.4 关键技术实现

#### JWT认证实现
```python
# settings/base.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

#### CORS配置
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True
```

#### 数据库优化
```python
# 查询优化示例
movies = Movie.objects.select_related('genre')\\
    .prefetch_related('reviews')\\
    .filter(rating__gte=9.0)\\
    .order_by('-rating')
```

---

## 🎨 前端开发详解

### 4.1 项目结构

```
frontend/
├── src/
│   ├── components/           # 可复用组件
│   │   ├── MovieCard.vue    # 电影卡片
│   │   ├── MovieChatBot.vue # AI聊天组件
│   │   └── Header.vue       # 页面头部
│   ├── views/               # 页面视图
│   │   ├── Home.vue        # 首页
│   │   ├── MovieList.vue   # 电影列表
│   │   ├── MovieDetail.vue # 电影详情
│   │   └── Login.vue       # 登录页
│   ├── services/            # API服务
│   │   ├── api.js          # Axios配置
│   │   ├── movieService.js # 电影API
│   │   └── authService.js  # 认证API
│   ├── stores/              # Pinia状态管理
│   │   └── auth.js         # 认证状态
│   ├── router/              # 路由配置
│   │   └── index.js
│   └── main.js             # 入口文件
├── public/
└── package.json
```

### 4.2 核心组件实现

#### MovieCard 组件
```vue
<template>
  <div class="movie-card">
    <img :src="posterUrl" :alt="movie.title"/>
    <div class="movie-info">
      <h3>{{ movie.title }}</h3>
      <div class="rating">⭐ {{ movie.rating }}</div>
      <p class="genres">{{ movie.genres.join(' / ') }}</p>
    </div>
  </div>
</template>
```

#### MovieChatBot 组件特色
- 🎯 右上角悬浮窗设计
- 💬 实时对话交互
- 🚀 快捷问题按钮
- 🎨 渐变色现代UI
- 📱 响应式布局

### 4.3 状态管理

使用Pinia进行状态管理：

```javascript
// stores/auth.js
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token')
  }),
  actions: {
    async login(credentials) {
      const data = await authService.login(credentials)
      this.token = data.access
      this.user = data.user
      localStorage.setItem('token', data.access)
    }
  }
})
```

### 4.4 路由配置

```javascript
const routes = [
  { path: '/', component: Home },
  { path: '/movies', component: MovieList },
  { path: '/movies/:id', component: MovieDetail },
  { 
    path: '/profile', 
    component: Profile,
    meta: { requiresAuth: true }  // 需要登录
  }
]
```

---

