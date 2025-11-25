# 🚀 AI聊天助手 - 快速启动指南

## ✅ 完成情况

**已为你创建以下文件**：

### 前端文件
1. ✅ `frontend/src/components/MovieChatBot.vue` - 悬浮窗聊天组件
2. ✅ `frontend/src/services/movieChat.js` - API服务
3. ✅ `frontend/src/views/Home.vue` - 已集成聊天组件

### 后端文件
4. ✅ `backend/apps/movies/views.py` - AI聊天API
5. ✅ `backend/apps/movies/urls.py` - URL路由配置
6. ✅ `backend/test_ai_chat.py` - 测试脚本

---

## 🎯 3步启动

### 步骤1：确保Ollama运行（服务器上）

```bash
# SSH连接到你的Ubuntu服务器
ssh root@你的服务器IP

# 检查Ollama状态
curl http://localhost:11434/api/tags

# 测试模型
ollama run movie-expert-v3 "杨丽老师是谁？"
```

**预期结果**：
```
杨丽老师是四川刘亦菲
```

---

### 步骤2：启动Django后端（本地）

```bash
# 打开终端1
cd d:\BYSJ\XM\bolg\blog\backend

# 启动Django
python manage.py runserver

# 看到这样的输出就成功了：
# Starting development server at http://127.0.0.1:8000/
```

**保持这个终端运行**

---

### 步骤3：启动Vue前端（本地）

```bash
# 打开终端2
cd d:\BYSJ\XM\bolg\blog\frontend

# 启动前端
npm run dev

# 看到这样的输出就成功了：
# VITE ready in XXX ms
# ➜  Local:   http://localhost:5173/
```

**保持这个终端运行**

---

## 🎉 开始使用

1. **打开浏览器**：访问 `http://localhost:5173`
2. **找到悬浮按钮**：页面右下角紫色渐变圆形按钮
3. **点击打开聊天**：展开聊天窗口
4. **开始对话**：
   - 点击快捷问题
   - 或输入任何关于电影的问题

---

## 🧪 测试API（可选）

### 方法1：使用测试脚本

```bash
cd d:\BYSJ\XM\bolg\blog\backend
python test_ai_chat.py
```

### 方法2：手动测试

```bash
# 测试聊天接口
curl -X POST http://localhost:8000/api/movies/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "杨丽老师是谁？"}'

# 测试推荐接口
curl -X POST http://localhost:8000/api/movies/recommend/ \
  -H "Content-Type: application/json" \
  -d '{"genre": "科幻"}'
```

---

## ❓ 常见问题

### Q1: 悬浮按钮没显示？

**检查**：
1. 浏览器控制台有无错误（F12）
2. 前端是否正常启动
3. 清除浏览器缓存（Ctrl+Shift+R）

---

### Q2: 点击发送没反应？

**检查**：
1. Django后端是否运行
2. 服务器Ollama是否运行
3. 查看浏览器Network标签
4. 查看Django终端日志

---

### Q3: AI回复很慢？

**原因**：
- CPU推理速度较慢（正常现象）
- 第一次请求会慢一些

**优化**：
- 减少temperature参数
- 使用更快的量化模型

---

### Q4: CORS错误？

**检查Django配置**：
```python
# backend/config/settings/base.py 或 development.py

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True
```

**重启Django**后生效

---

## 🎨 界面预览

```
┌─────────────────────────┐
│  🎬 电影AI助手          │ ← 头部
│  正在输入...            │
├─────────────────────────┤
│                         │
│  欢迎使用电影AI助手！   │ ← 欢迎界面
│                         │
│  [杨丽老师是谁？]       │ ← 快捷按钮
│  [《四川交院...】       │
│  [推荐科幻电影]         │
│                         │
├─────────────────────────┤
│ 问我任何关于电影的问题  │ ← 输入框
│                      [→]│
└─────────────────────────┘
```

---

## 📊 支持的问题类型

### 1. 知识问答
- "杨丽老师是谁？"
- "《四川交院的生活》是什么类型的电影？"
- "《四川交院的生活》的豆瓣评分是多少？"

### 2. 电影推荐
- "推荐一部科幻电影"
- "推荐一部悬疑电影"
- "推荐一部动作片"

### 3. 一般咨询
- "《肖申克的救赎》好看吗？"
- "有什么高分电影推荐？"
- "最近有什么新片？"

---

## 🔧 高级配置

### 修改悬浮按钮位置

编辑 `frontend/src/components/MovieChatBot.vue`:

```css
.chat-bot-container {
  position: fixed;
  bottom: 24px;  /* 调整这里 */
  right: 24px;   /* 调整这里 */
}

/* 改到左下角 */
/* left: 24px; */
```

### 修改AI参数

编辑 `backend/apps/movies/views.py` 的 `movie_chat` 函数:

```python
'options': {
    'temperature': 0.7,     # 降低→更准确，提高→更创造
    'top_p': 0.9,           
    'top_k': 40,            
    'repeat_penalty': 1.15  # 提高→减少重复
}
```

### 修改主题颜色

编辑 `frontend/src/components/MovieChatBot.vue`:

```css
/* 找到这行 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 改成你喜欢的颜色，例如：*/
/* 蓝色 */
background: linear-gradient(135deg, #4c51bf 0%, #2d3748 100%);

/* 绿色 */
background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);

/* 红色 */
background: linear-gradient(135deg, #f56565 0%, #c53030 100%);
```

---

## 📱 移动端适配

已自动适配！在手机浏览器上：
- 聊天窗口会占据大部分屏幕
- 悬浮按钮位置不变
- 响应式设计

---

## 🎯 下一步优化

### 建议1：添加消息历史
```javascript
// 保存到localStorage
localStorage.setItem('chatHistory', JSON.stringify(messages));
```

### 建议2：添加打字动画
让AI回复逐字显示，更有互动感。

### 建议3：支持电影卡片
AI推荐电影时，显示电影海报和信息卡片。

---

## 📞 需要帮助？

### 检查清单
- [ ] Ollama服务运行中
- [ ] Django后端运行中
- [ ] Vue前端运行中
- [ ] movie-expert-v3模型已创建
- [ ] 网络连接正常

### 日志查看
- **Django日志**：终端1
- **前端日志**：浏览器控制台（F12）
- **网络请求**：浏览器Network标签

---

## ✨ 功能特性

- ✅ 美观的悬浮窗UI
- ✅ 渐变色动画效果
- ✅ 打字中提示
- ✅ 快捷问题按钮
- ✅ 消息时间戳
- ✅ 错误处理
- ✅ 响应式设计
- ✅ 移动端适配

---

**现在就试试吧！** 🚀

1. 启动Django → `python manage.py runserver`
2. 启动Vue → `npm run dev`
3. 访问 `http://localhost:5173`
4. 点击右下角悬浮按钮
5. 开始聊天！🎬
