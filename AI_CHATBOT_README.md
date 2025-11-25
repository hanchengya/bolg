# 🎬 电影AI助手集成指南

## ✅ 已完成的工作

### 1. 前端组件
- ✅ **MovieChatBot.vue** - 悬浮窗聊天组件
  - 位置：`frontend/src/components/MovieChatBot.vue`
  - 功能：漂亮的悬浮窗UI、消息历史、快捷问题
  - 样式：渐变色、动画效果、响应式设计

### 2. 前端服务
- ✅ **movieChat.js** - API服务层
  - 位置：`frontend/src/services/movieChat.js`
  - 功能：与后端API通信、错误处理

### 3. 后端API
- ✅ **movie_chat** - 聊天接口
  - URL: `POST /api/movies/chat/`
  - 功能：接收用户消息，调用Ollama返回AI回复
  
- ✅ **movie_recommend** - 推荐接口
  - URL: `POST /api/movies/recommend/`
  - 功能：根据类型推荐电影

### 4. 页面集成
- ✅ **Home.vue** - 首页已添加聊天组件
  - 位置：右下角悬浮

---

## 🚀 启动步骤

### 1. 确保Ollama服务运行中

在服务器上：
```bash
# 检查Ollama是否运行
curl http://localhost:11434/api/generate -d '{
  "model": "movie-expert-v3",
  "prompt": "你好",
  "stream": false
}'

# 如果没运行，启动Ollama
ollama serve
```

### 2. 启动Django后端

```bash
cd d:\BYSJ\XM\bolg\blog\backend

# 激活虚拟环境（如果有）
# source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 启动开发服务器
python manage.py runserver
```

### 3. 启动Vue前端

```bash
cd d:\BYSJ\XM\bolg\blog\frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问网站

浏览器打开：`http://localhost:5173`

---

## 🎨 使用方法

### 用户角度

1. **打开首页** - 右下角会看到紫色渐变的悬浮按钮
2. **点击按钮** - 展开聊天窗口
3. **快捷问题** - 点击预设问题快速提问
4. **自由对话** - 输入任何关于电影的问题

### 支持的问题类型

- ✅ "杨丽老师是谁？"
- ✅ "《四川交院的生活》是什么类型的电影？"
- ✅ "推荐一部科幻电影"
- ✅ "《肖申克的救赎》好看吗？"
- ✅ "有哪些高分悬疑片？"

---

## 🔧 配置选项

### 调整AI参数

在 `backend/apps/movies/views.py` 的 `movie_chat` 函数中：

```python
'options': {
    'temperature': 0.7,     # 创造性：0.1-1.0（越高越随机）
    'top_p': 0.9,           # 多样性：0.1-1.0
    'top_k': 40,            # 候选词数量
    'repeat_penalty': 1.15  # 重复惩罚：1.0-2.0
}
```

### 修改悬浮窗位置

在 `frontend/src/components/MovieChatBot.vue` 中：

```css
.chat-bot-container {
  position: fixed;
  bottom: 24px;    /* 调整底部距离 */
  right: 24px;     /* 调整右侧距离 */
  /* 改为左侧：left: 24px; */
}
```

### 修改主题颜色

```css
/* 修改渐变色 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 改为其他颜色，例如：*/
/* 蓝色：#667eea -> #4c51bf */
/* 绿色：#48bb78 -> #38a169 */
/* 红色：#f56565 -> #c53030 */
```

---

## 🐛 常见问题

### 1. AI无响应

**问题**：点击发送后一直显示"正在输入..."

**解决**：
```bash
# 检查Ollama服务
curl http://localhost:11434/api/tags

# 检查模型是否存在
ollama list | grep movie-expert-v3

# 重启Ollama
ollama serve
```

### 2. CORS错误

**问题**：浏览器控制台显示CORS错误

**解决**：检查Django CORS配置
```python
# backend/config/settings/base.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### 3. 悬浮窗不显示

**问题**：首页看不到悬浮按钮

**解决**：
1. 检查浏览器控制台错误
2. 确认组件已正确导入
3. 清除浏览器缓存
4. 重启前端开发服务器

### 4. 响应速度慢

**问题**：AI回复需要很长时间

**优化**：
1. 降低temperature参数
2. 减少max_tokens
3. 使用更快的量化模型（q4_0）
4. 升级服务器硬件

---

## 📊 API文档

### POST /api/movies/chat/

**请求**：
```json
{
  "message": "杨丽老师是谁？"
}
```

**响应（成功）**：
```json
{
  "success": true,
  "response": "杨丽老师是四川刘亦菲"
}
```

**响应（失败）**：
```json
{
  "success": false,
  "error": "错误信息"
}
```

### POST /api/movies/recommend/

**请求**：
```json
{
  "genre": "科幻"
}
```

**响应**：
```json
{
  "success": true,
  "recommendation": "推荐《星际穿越》..."
}
```

---

## 🎯 后续优化建议

### 功能增强
- [ ] 添加消息历史记录（localStorage）
- [ ] 支持多轮对话上下文
- [ ] 添加语音输入功能
- [ ] 支持表情符号
- [ ] 添加打字动画效果
- [ ] 支持电影卡片展示
- [ ] 添加夜间模式切换

### 性能优化
- [ ] 实现消息缓存（Redis）
- [ ] 添加请求防抖
- [ ] 实现流式响应
- [ ] 使用WebSocket实时通信
- [ ] 添加加载骨架屏

### 用户体验
- [ ] 添加消息已读标记
- [ ] 支持消息编辑/删除
- [ ] 添加快捷回复
- [ ] 支持消息搜索
- [ ] 添加消息导出功能

---

## 📝 技术栈

- **前端**: Vue 3 + Vite + TailwindCSS
- **后端**: Django + Django REST Framework
- **AI模型**: Ollama + movie-expert-v3
- **通信**: Axios + REST API

---

## 🔐 安全建议

1. **生产环境配置**：
   - 启用Django的CSRF保护
   - 配置正确的CORS域名
   - 使用HTTPS
   - 添加请求频率限制

2. **API安全**：
   - 添加用户认证（可选）
   - 实现请求限流
   - 记录异常请求
   - 过滤敏感词

---

## 💡 使用提示

### 最佳实践

1. **提问技巧**：
   - 问题要具体明确
   - 一次只问一个问题
   - 可以要求更详细的解释

2. **性能优化**：
   - 关闭不用的聊天窗口
   - 定期清理历史消息
   - 避免频繁刷新页面

3. **问题调试**：
   - 查看浏览器控制台
   - 检查网络请求
   - 查看Django日志

---

## 📞 技术支持

如有问题，请检查：
1. Django后端日志
2. 浏览器开发者工具
3. Ollama服务状态
4. 网络连接

---

**祝使用愉快！🎉**
