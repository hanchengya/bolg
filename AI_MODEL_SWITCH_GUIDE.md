# AI 模型切换功能使用指南

## 功能概述

管理员可以在后台界面实时切换 AI 聊天使用的模型，无需重启服务器。

## 功能特点

✅ **实时切换** - 切换后立即生效，所有用户聊天使用新模型  
✅ **可视化管理** - 清晰显示所有可用模型及其状态  
✅ **权限控制** - 仅管理员可以切换模型  
✅ **持久化配置** - 切换的模型会自动保存到配置文件  

## 访问路径

1. 登录管理员账户
2. 进入管理员控制台: `http://localhost:5173/admin`
3. 点击 **🤖 AI模型** 标签页

## 界面功能

### 当前模型显示
- 顶部显著位置展示当前正在使用的模型
- 所有用户的 AI 聊天将使用此模型

### 模型列表
每个模型显示以下信息：
- **名称**: 模型的完整名称
- **大小**: 模型文件大小
- **更新时间**: 模型的最后修改时间
- **状态标记**: 当前使用的模型会高亮显示

### 操作按钮
- **切换**: 点击切换到该模型
- **刷新**: 重新加载模型列表
- **使用中**: 当前模型（无法切换）

## API 端点

### 1. 获取可用模型列表
```http
GET /api/movies/models/
```

**响应示例:**
```json
{
  "success": true,
  "models": [
    {
      "name": "movie-expert-v3:latest",
      "size": "6.84 GB",
      "modified_at": "2025-11-24T12:29:37...",
      "is_current": true
    }
  ],
  "current_model": "movie-expert-v3"
}
```

### 2. 切换模型（需要管理员权限）
```http
POST /api/movies/models/switch/
Authorization: Bearer <token>
Content-Type: application/json

{
  "model_name": "movie-expert-v3:latest"
}
```

**响应示例:**
```json
{
  "success": true,
  "message": "已切换到模型: movie-expert-v3:latest",
  "current_model": "movie-expert-v3:latest"
}
```

### 3. 获取当前模型
```http
GET /api/movies/models/current/
```

**响应示例:**
```json
{
  "success": true,
  "current_model": "movie-expert-v3"
}
```

## 技术实现

### 后端实现
- 文件: `backend/apps/movies/views.py`
- 使用全局变量 `CURRENT_MODEL` 存储当前模型
- 切换时自动更新 `ai_config.py` 配置文件
- 支持热切换，无需重启服务器

### 前端实现
- 组件: `frontend/src/components/AdminAIModels.vue`
- 页面: `frontend/src/views/Admin.vue`
- 实时加载和显示模型列表
- 提供直观的切换界面

## 可用模型

当前系统中可用的电影 AI 模型：

1. **movie-expert-v3** (6.84 GB) - 最新的电影专家模型
2. **movie-expert** (6.84 GB) - 基础电影专家模型
3. **movie-qwen-full** (4.36 GB) - Qwen 完整版
4. **movie-qwen** (4.36 GB) - Qwen 基础版
5. **movie-deepseek** (4.36 GB) - DeepSeek 版本

## 使用建议

1. **选择专业模型**: 优先选择名称包含 "movie-expert" 的模型
2. **考虑性能**: 较大的模型可能响应更慢但准确性更高
3. **测试效果**: 切换后可以在前端聊天界面测试效果
4. **高峰期谨慎**: 避免在用户活跃时段频繁切换

## 故障排除

### 问题: 无法加载模型列表
- 检查 Ollama 服务是否运行: `http://10.5.80.8:11434`
- 检查网络连接
- 查看后端日志

### 问题: 切换失败
- 确认是否以管理员身份登录
- 检查模型名称是否正确
- 查看浏览器控制台错误信息

### 问题: 切换后没有生效
- 刷新前端页面
- 检查 `ai_config.py` 是否更新
- 重启后端服务器

## 测试命令

运行测试脚本验证 API:
```bash
python test_model_api.py
```

测试 AI 聊天功能:
```bash
python test_chat_api.py
```

## 更新日志

### v1.0 (2025-11-25)
- ✅ 实现模型管理后端 API
- ✅ 创建管理员界面组件
- ✅ 支持实时切换模型
- ✅ 添加权限控制
- ✅ 配置文件自动更新

## 未来计划

- [ ] 添加模型性能统计
- [ ] 支持自定义模型参数
- [ ] 模型使用历史记录
- [ ] 模型效果评分系统
