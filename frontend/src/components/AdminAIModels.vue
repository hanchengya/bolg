<template>
  <div class="ai-models-management">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">🤖 AI 模型管理</h2>
      <button
        @click="refreshModels"
        :disabled="loading"
        class="px-4 py-2 bg-accent-primary text-white rounded-lg hover:bg-accent-secondary transition disabled:opacity-50"
      >
        {{ loading ? '刷新中...' : '🔄 刷新' }}
      </button>
    </div>

    <!-- 当前使用的模型 -->
    <div class="bg-gradient-to-r from-accent-primary/20 to-accent-secondary/20 p-6 rounded-lg mb-6 border border-accent-primary/30">
      <div class="flex items-center gap-3 mb-2">
        <span class="text-2xl">⭐</span>
        <h3 class="text-xl font-semibold">当前模型</h3>
      </div>
      <p class="text-2xl font-bold text-accent-primary">{{ currentModel || '加载中...' }}</p>
      <p class="text-sm text-gray-400 mt-2">所有用户的 AI 聊天将使用此模型</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-accent-primary"></div>
      <p class="text-gray-400 mt-4">加载模型列表中...</p>
    </div>

    <!-- 错误信息 -->
    <div v-else-if="error" class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-lg mb-6">
      <p>⚠️ {{ error }}</p>
    </div>

    <!-- 模型列表 -->
    <div v-else class="space-y-4">
      <div
        v-for="model in models"
        :key="model.name"
        class="bg-bg-secondary p-6 rounded-lg border transition-all"
        :class="model.is_current ? 'border-accent-primary shadow-lg shadow-accent-primary/20' : 'border-gray-700 hover:border-gray-600'"
      >
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="text-xl font-bold">{{ model.name }}</h3>
              <span
                v-if="model.is_current"
                class="px-3 py-1 bg-accent-primary text-white text-xs rounded-full font-semibold"
              >
                当前使用
              </span>
            </div>
            <div class="flex items-center gap-6 text-sm text-gray-400">
              <span>📦 大小: {{ model.size }}</span>
              <span>🕒 更新: {{ formatDate(model.modified_at) }}</span>
            </div>
          </div>
          <button
            v-if="!model.is_current"
            @click="switchToModel(model.name)"
            :disabled="switching"
            class="px-6 py-2 bg-accent-primary text-white rounded-lg hover:bg-accent-secondary transition disabled:opacity-50 font-semibold"
          >
            {{ switching ? '切换中...' : '切换' }}
          </button>
          <div v-else class="px-6 py-2 bg-green-500/20 text-green-400 rounded-lg font-semibold">
            ✓ 使用中
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="models.length === 0" class="text-center py-12 text-gray-400">
        <p class="text-xl mb-2">📦</p>
        <p>暂无可用的电影 AI 模型</p>
      </div>
    </div>

    <!-- 提示信息 -->
    <div class="mt-8 bg-blue-500/10 border border-blue-500/30 text-blue-400 p-4 rounded-lg">
      <p class="font-semibold mb-2">💡 提示：</p>
      <ul class="text-sm space-y-1 list-disc list-inside">
        <li>切换模型后会立即生效，所有用户将使用新模型</li>
        <li>建议选择名称包含 "movie-expert" 的专业电影模型</li>
        <li>较大的模型可能响应更慢但准确性更高</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api/movies';

const models = ref([]);
const currentModel = ref('');
const loading = ref(false);
const switching = ref(false);
const error = ref('');

// 获取模型列表
const loadModels = async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await axios.get(`${API_BASE}/models/`);
    if (response.data.success) {
      models.value = response.data.models;
      currentModel.value = response.data.current_model;
    } else {
      error.value = response.data.error || '获取模型列表失败';
    }
  } catch (err) {
    error.value = err.response?.data?.error || '无法连接到服务器';
    console.error('加载模型失败:', err);
  } finally {
    loading.value = false;
  }
};

// 刷新模型列表
const refreshModels = () => {
  loadModels();
};

// 切换模型
const switchToModel = async (modelName) => {
  if (!confirm(`确定要切换到模型 "${modelName}" 吗？\n\n切换后，所有用户的 AI 聊天将立即使用新模型。`)) {
    return;
  }

  switching.value = true;
  error.value = '';
  
  try {
    const token = localStorage.getItem('access_token');
    const response = await axios.post(
      `${API_BASE}/models/switch/`,
      { model_name: modelName },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    if (response.data.success) {
      alert(`✅ ${response.data.message}`);
      currentModel.value = response.data.current_model;
      // 刷新列表
      await loadModels();
    } else {
      alert(`❌ ${response.data.error || '切换失败'}`);
    }
  } catch (err) {
    const errorMsg = err.response?.data?.error || '切换模型失败';
    alert(`❌ ${errorMsg}`);
    console.error('切换模型失败:', err);
  } finally {
    switching.value = false;
  }
};

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知';
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch {
    return dateString;
  }
};

onMounted(() => {
  loadModels();
});
</script>

<style scoped>
.ai-models-management {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
