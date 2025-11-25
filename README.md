# 电影博客网站项目

> 基于Django REST Framework + Vue.js 3的现代化电影社区平台
>
> 数据来源：豆瓣Top250电影

---

## 🎬 项目简介

这是一个功能完整的电影博客网站，允许用户浏览豆瓣Top250电影、发布影评、评分、创建观影清单等功能。采用前后端分离架构，后端使用Django REST Framework提供API服务，前端使用Vue.js 3构建用户界面。

### 核心功能

- 🎥 **电影展示** - 展示豆瓣Top250电影，支持搜索和多维度筛选
- 📝 **影评系统** - 用户可以发表影评、评论和回复
- ⭐ **评分系统** - 用户可以为电影打分，系统自动计算平均分
- 📋 **观影清单** - 管理想看/在看/已看的电影
- 👤 **用户系统** - 注册、登录、个人资料管理
- 🔐 **JWT认证** - 安全的Token认证机制

---

## 📁 项目结构

```
blog/
├── backend/                      # Django后端 ✅ 已完成
│   ├── config/                   # 项目配置
│   ├── apps/                     # Django应用
│   │   ├── users/               # 用户系统
│   │   ├── movies/              # 电影系统
│   │   ├── reviews/             # 影评系统
│   │   ├── ratings/             # 评分系统
│   │   └── watchlists/          # 观影清单
│   ├── media/                    # 媒体文件
│   ├── scripts/                  # 工具脚本
│   ├── requirements.txt          # Python依赖
│   ├── manage.py
│   └── README.md                # 后端说明文档
├── frontend/                     # Vue.js前端 ⏳ 待开发
├── douban_top250/               # 电影数据
│   ├── douban_top250.json       # 250部电影数据
│   ├── douban_top250.md         # 电影列表文档
│   └── images/                  # 250张电影海报
├── plan.md                       # 技术设计方案（完整）
├── PROGRESS.md                   # 开发进度记录
├── test.md                       # 测试报告
├── CLAUDE.md                     # 开发指导
└── README.md                     # 项目说明（本文件）
```

---

## 🚀 技术栈

### 后端技术

- **框架**: Django 4.2.7 + Django REST Framework 3.14.0
- **数据库**: MySQL 8.0+ (10.5.80.8:3306)
- **缓存**: Redis 7+
- **认证**: JWT (djangorestframework-simplejwt)
- **API文档**: drf-spectacular (Swagger UI)
- **其他**: CORS、django-filter、Pillow

### 前端技术（计划）

- **框架**: Vue.js 3 (Composition API)
- **构建**: Vite 5+
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **UI框架**: Tailwind CSS 3 + Flowbite Vue
- **HTTP**: Axios

---

## 📊 数据库设计

### 数据表

- `users_user` - 用户表（扩展Django User）
- `movies_movie` - 电影表（250部豆瓣Top250电影）
- `movies_genre` - 电影类型表
- `reviews_review` - 影评表
- `reviews_comment` - 评论表
- `ratings_rating` - 评分表
- `watchlists_watchlist` - 观影清单表

### 数据库配置

```
主机: 10.5.80.8
端口: 3306
数据库: moviedb
用户: root
密码: 123456
字符集: utf8mb4
```

---

## 🛠️ 快速开始

### 后端安装

1. **创建虚拟环境**

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置环境变量**

```bash
cp .env.example .env
# 根据需要修改.env文件
```

4. **创建数据库**

在MySQL中执行：

```sql
CREATE DATABASE IF NOT EXISTS moviedb
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

5. **运行数据库迁移**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **创建超级用户**

```bash
python manage.py createsuperuser
```

7. **导入豆瓣Top250数据**

```bash
python scripts/import_douban_data.py
```

8. **启动开发服务器**

```bash
python manage.py runserver
```

9. **访问API文档**

- Swagger UI: http://localhost:8000/api/docs/
- Django Admin: http://localhost:8000/admin/

---

## 📚 API文档

### 认证相关

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/register/` | 用户注册 |
| POST | `/api/v1/auth/login/` | 用户登录 |
| POST | `/api/v1/auth/refresh/` | 刷新Token |
| GET | `/api/v1/auth/me/` | 获取当前用户 |
| PUT | `/api/v1/auth/me/` | 更新个人资料 |
| POST | `/api/v1/auth/change-password/` | 修改密码 |

### 电影相关

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/movies/` | 电影列表（支持筛选） |
| GET | `/api/v1/movies/{id}/` | 电影详情 |
| GET | `/api/v1/movies/top_rated/` | 高分电影 |
| GET | `/api/v1/movies/search/?q=关键词` | 搜索电影 |

### 影评相关

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/reviews/` | 影评列表 |
| POST | `/api/v1/reviews/` | 创建影评 |
| GET | `/api/v1/reviews/{id}/` | 影评详情 |
| PUT | `/api/v1/reviews/{id}/` | 更新影评 |
| DELETE | `/api/v1/reviews/{id}/` | 删除影评 |
| POST | `/api/v1/reviews/{id}/helpful/` | 标记有用 |

### 评分相关

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/ratings/` | 我的评分列表 |
| POST | `/api/v1/ratings/` | 评分/更新评分 |

### 观影清单

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/watchlist/` | 我的观影清单 |
| POST | `/api/v1/watchlist/` | 添加到清单 |
| PUT | `/api/v1/watchlist/{id}/` | 更新状态 |
| DELETE | `/api/v1/watchlist/{id}/` | 移除 |

完整API文档请访问: http://localhost:8000/api/docs/

---

## ✨ 功能特点

### 已实现功能（后端）

- ✅ 完整的RESTful API设计
- ✅ JWT Token认证机制
- ✅ 用户注册、登录、个人资料管理
- ✅ 电影列表、详情、搜索、筛选
- ✅ 影评发布、编辑、删除、评论
- ✅ 电影评分，自动计算平均分
- ✅ 观影清单管理（想看/在看/已看）
- ✅ Swagger API文档
- ✅ CORS跨域支持
- ✅ Redis缓存配置
- ✅ 数据库查询优化
- ✅ 豆瓣Top250数据导入工具

### 待开发功能（前端）

- ⏳ Vue.js 3用户界面
- ⏳ 响应式设计（移动端适配）
- ⏳ 瀑布流电影展示
- ⏳ 用户登录/注册界面
- ⏳ 电影详情页
- ⏳ 影评浏览和发布
- ⏳ 个人中心
- ⏳ 观影清单管理界面

---

## 📈 开发进度

### 后端开发：100% ✅

- ✅ Django项目初始化
- ✅ 数据库模型设计
- ✅ API接口实现（25+个端点）
- ✅ JWT认证系统
- ✅ 数据导入工具
- ✅ API文档生成
- ✅ 单元测试验证

### 前端开发：0% ⏳

- ⏳ Vue.js项目初始化
- ⏳ 路由和状态管理配置
- ⏳ UI组件开发
- ⏳ 页面实现
- ⏳ 前后端联调

详细进度请查看: [PROGRESS.md](PROGRESS.md)

---

## 📝 项目文档

- **技术设计方案**: [plan.md](plan.md) - 完整的技术架构和设计文档
- **开发进度记录**: [PROGRESS.md](PROGRESS.md) - 详细的开发日志
- **测试报告**: [test.md](test.md) - 功能测试和验证报告
- **后端文档**: [backend/README.md](backend/README.md) - 后端安装和使用说明
- **开发指导**: [CLAUDE.md](CLAUDE.md) - 项目开发规范

---

## 🎯 项目统计

- **代码文件**: 40+ 个Python文件
- **代码量**: 约3000+行
- **数据模型**: 7个
- **API端点**: 25+个
- **电影数据**: 250部（豆瓣Top250）
- **电影海报**: 250张高清图片

---

## 🔐 安全特性

- ✅ JWT Token认证
- ✅ 密码加密存储
- ✅ CORS安全配置
- ✅ SQL注入防护（Django ORM）
- ✅ CSRF保护
- ✅ 密码强度验证
- ✅ 环境变量隔离

---

## 🤝 贡献指南

本项目目前处于开发阶段，欢迎贡献代码或提出建议。

### 开发流程

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📄 许可证

MIT License

---

## 👨‍💻 作者

- 开发者: Claude AI
- 开发日期: 2025-11-14
- 项目类型: 毕业设计/学习项目

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 查看技术文档: [plan.md](plan.md)
- 查看开发进度: [PROGRESS.md](PROGRESS.md)
- 查看测试报告: [test.md](test.md)

---

## 🙏 致谢

- 感谢豆瓣电影提供的电影数据
- 感谢Django和Vue.js社区
- 感谢所有开源项目的贡献者

---

**项目状态**: 后端开发完成 ✅ | 前端开发中 ⏳

**最后更新**: 2025-11-14
