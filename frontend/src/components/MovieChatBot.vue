<template>
  <div class="chat-bot-container">
    <!-- 悬浮按钮 -->
    <transition name="bounce">
      <button
        v-if="!isOpen"
        @click="toggleChat"
        class="chat-button"
        title="电影AI助手"
      >
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
        </svg>
        <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
      </button>
    </transition>

    <!-- 聊天窗口 -->
    <transition name="slide-up">
      <div v-if="isOpen" class="chat-window">
        <!-- 头部 -->
        <div class="chat-header">
          <div class="flex items-center gap-3">
            <div class="avatar">
              <span class="text-2xl">🎬</span>
            </div>
            <div>
              <h3 class="font-bold text-lg">电影AI助手</h3>
              <p class="text-xs text-gray-400">
                <span v-if="isTyping" class="typing-indicator">正在输入...</span>
                <span v-else>{{ statusText }}</span>
              </p>
            </div>
          </div>
          <button @click="toggleChat" class="close-button">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- 消息列表 -->
        <div class="chat-messages" ref="messagesContainer">
          <!-- 欢迎消息 -->
          <div v-if="messages.length === 0" class="welcome-message">
            <div class="text-4xl mb-4">🎬</div>
            <h4 class="text-xl font-bold mb-2">欢迎使用电影AI助手！</h4>
            <p class="text-gray-400 mb-4">我可以帮你：</p>
            <div class="suggestions">
              <button @click="sendQuickMessage('杨丽老师是谁？')" class="suggestion-btn">
                杨丽老师是谁？
              </button>
              <button @click="sendQuickMessage('《四川交院的生活》是什么类型的电影？')" class="suggestion-btn">
                《四川交院的生活》介绍
              </button>
              <button @click="sendQuickMessage('推荐一部科幻电影')" class="suggestion-btn">
                推荐科幻电影
              </button>
              <button @click="sendQuickMessage('推荐一部悬疑电影')" class="suggestion-btn">
                推荐悬疑电影
              </button>
            </div>
          </div>

          <!-- 聊天消息 -->
          <div
            v-for="(msg, index) in messages"
            :key="index"
            :class="['message', msg.type]"
          >
            <div class="message-avatar">
              <span v-if="msg.type === 'user'">👤</span>
              <span v-else>🎬</span>
            </div>
            <div class="message-content">
              <div class="message-bubble">
                {{ msg.text }}
              </div>
              <div class="message-time">{{ msg.time }}</div>
            </div>
          </div>

          <!-- 输入中提示 -->
          <div v-if="isTyping" class="message ai">
            <div class="message-avatar">🎬</div>
            <div class="message-content">
              <div class="message-bubble typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入框 -->
        <div class="chat-input">
          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="问我任何关于电影的问题..."
            :disabled="isTyping"
            class="input-field"
          />
          <button
            @click="sendMessage"
            :disabled="!inputMessage.trim() || isTyping"
            class="send-button"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, nextTick, computed } from 'vue';
import { movieChatService } from '../services/movieChat';

const isOpen = ref(true);  // 默认打开
const messages = ref([]);
const inputMessage = ref('');
const isTyping = ref(false);
const messagesContainer = ref(null);
const unreadCount = ref(0);

const statusText = computed(() => {
  if (messages.value.length === 0) {
    return '在线 - 随时为您服务';
  }
  return '在线';
});

const toggleChat = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    unreadCount.value = 0;
  }
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

const getCurrentTime = () => {
  const now = new Date();
  return now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
};

const sendQuickMessage = (text) => {
  inputMessage.value = text;
  sendMessage();
};

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isTyping.value) return;

  const userMessage = inputMessage.value.trim();
  
  // 添加用户消息
  messages.value.push({
    type: 'user',
    text: userMessage,
    time: getCurrentTime()
  });

  inputMessage.value = '';
  scrollToBottom();

  // 显示输入中状态
  isTyping.value = true;

  try {
    // 调用AI接口
    const response = await movieChatService.sendMessage(userMessage);
    
    // 添加AI回复
    messages.value.push({
      type: 'ai',
      text: response,
      time: getCurrentTime()
    });

    // 如果窗口关闭，增加未读计数
    if (!isOpen.value) {
      unreadCount.value++;
    }
  } catch (error) {
    console.error('AI回复失败:', error);
    messages.value.push({
      type: 'ai',
      text: '抱歉，我现在无法回答。请稍后再试。',
      time: getCurrentTime()
    });
  } finally {
    isTyping.value = false;
    scrollToBottom();
  }
};
</script>

<style scoped>
.chat-bot-container {
  position: fixed;
  top: 80px;
  right: 24px;
  z-index: 1000;
}

/* 悬浮按钮 */
.chat-button {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
  position: relative;
  cursor: pointer;
  border: none;
}

.chat-button:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6);
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ef4444;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

/* 聊天窗口 */
.chat-window {
  width: 420px;
  height: 600px;
  background: #1a1a2e;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 头部 */
.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  transition: all 0.2s;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
}

.typing-indicator {
  color: #a0aec0;
  font-style: italic;
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #16213e;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 3px;
}

/* 欢迎消息 */
.welcome-message {
  text-align: center;
  padding: 40px 20px;
  color: white;
}

.suggestions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 20px;
}

.suggestion-btn {
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.4);
  color: white;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  font-size: 14px;
}

.suggestion-btn:hover {
  background: rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

/* 消息 */
.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(102, 126, 234, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 20px;
}

.message-content {
  max-width: 70%;
}

.message.user .message-content {
  text-align: right;
}

.message-bubble {
  background: rgba(102, 126, 234, 0.2);
  padding: 12px 16px;
  border-radius: 16px;
  color: white;
  word-wrap: break-word;
  line-height: 1.5;
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.message-time {
  font-size: 11px;
  color: #a0aec0;
  margin-top: 4px;
  padding: 0 4px;
}

/* 输入中动画 */
.message-bubble.typing {
  display: flex;
  gap: 4px;
  padding: 16px;
}

.message-bubble.typing span {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.message-bubble.typing span:nth-child(2) {
  animation-delay: 0.2s;
}

.message-bubble.typing span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

/* 输入框 */
.chat-input {
  padding: 16px 20px;
  background: #1a1a2e;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  display: flex;
  gap: 12px;
}

.input-field {
  flex: 1;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 24px;
  padding: 12px 20px;
  color: white;
  outline: none;
  transition: all 0.2s;
}

.input-field:focus {
  background: rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.input-field::placeholder {
  color: #a0aec0;
}

.send-button {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 动画 */
.bounce-enter-active {
  animation: bounce-in 0.5s;
}

.bounce-leave-active {
  animation: bounce-in 0.3s reverse;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.slide-up-enter-active {
  animation: slide-up 0.3s ease-out;
}

.slide-up-leave-active {
  animation: slide-up 0.3s ease-in reverse;
}

@keyframes slide-up {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .chat-window {
    width: calc(100vw - 48px);
    height: calc(100vh - 120px);
  }
}
</style>
