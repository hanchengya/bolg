<template>
  <div class="debug-page p-8">
    <h1 class="text-4xl font-bold mb-6 text-accent-primary">🔍 API调试页面</h1>
    
    <div class="mb-6 bg-bg-secondary p-4 rounded-lg">
      <h2 class="text-2xl font-bold mb-4">测试控制</h2>
      <button 
        @click="testAPI" 
        class="bg-accent-secondary hover:bg-red-700 text-white px-6 py-3 rounded-lg mr-4"
      >
        测试API连接
      </button>
      <button 
        @click="clearLogs" 
        class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg"
      >
        清除日志
      </button>
    </div>

    <!-- 状态显示 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-bg-secondary p-4 rounded-lg">
        <h3 class="font-bold mb-2">API基础URL</h3>
        <p class="text-accent-primary">{{ apiBaseURL }}</p>
      </div>
      <div class="bg-bg-secondary p-4 rounded-lg">
        <h3 class="font-bold mb-2">测试状态</h3>
        <p :class="testStatus.color">{{ testStatus.text }}</p>
      </div>
      <div class="bg-bg-secondary p-4 rounded-lg">
        <h3 class="font-bold mb-2">电影数量</h3>
        <p class="text-2xl font-bold text-accent-primary">{{ movieCount }}</p>
      </div>
    </div>

    <!-- 日志输出 -->
    <div class="bg-bg-secondary p-6 rounded-lg mb-6">
      <h2 class="text-2xl font-bold mb-4">测试日志</h2>
      <div class="bg-gray-900 p-4 rounded max-h-96 overflow-y-auto font-mono text-sm">
        <div v-for="(log, index) in logs" :key="index" :class="log.class" class="mb-2">
          <span class="text-gray-500">[{{ log.time }}]</span> {{ log.message }}
        </div>
        <div v-if="logs.length === 0" class="text-gray-500">
          点击"测试API连接"开始测试...
        </div>
      </div>
    </div>

    <!-- 电影数据展示 -->
    <div v-if="movies.length > 0" class="bg-bg-secondary p-6 rounded-lg">
      <h2 class="text-2xl font-bold mb-4">获取到的电影数据 (前5部)</h2>
      <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div v-for="movie in movies.slice(0, 5)" :key="movie.id" class="bg-gray-800 p-4 rounded-lg">
          <img 
            :src="movie.poster" 
            :alt="movie.title"
            class="w-full h-48 object-cover rounded mb-2"
            @error="handleImageError"
          />
          <h3 class="font-bold text-sm mb-1 line-clamp-2">{{ movie.title }}</h3>
          <p class="text-accent-primary">⭐ {{ movie.douban_rating }}</p>
          <p class="text-gray-400 text-xs">排名: {{ movie.rank }}</p>
        </div>
      </div>
    </div>

    <!-- 原始响应数据 -->
    <div v-if="rawResponse" class="bg-bg-secondary p-6 rounded-lg mt-6">
      <h2 class="text-2xl font-bold mb-4">原始API响应</h2>
      <pre class="bg-gray-900 p-4 rounded overflow-x-auto text-xs">{{ rawResponse }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { movieService } from '../services/movies';
import axios from 'axios';

const logs = ref([]);
const movies = ref([]);
const rawResponse = ref(null);
const movieCount = ref(0);
const apiBaseURL = ref('http://localhost:8000/api/v1');

const testStatus = computed(() => {
  if (movies.value.length > 0) {
    return { text: '✅ 成功', color: 'text-green-500 text-xl font-bold' };
  }
  return { text: '⏳ 未测试', color: 'text-gray-400' };
});

function addLog(message, type = 'info') {
  const time = new Date().toLocaleTimeString();
  const colorClass = {
    'info': 'text-blue-400',
    'success': 'text-green-500',
    'error': 'text-red-500',
    'warning': 'text-yellow-500'
  }[type] || 'text-gray-300';
  
  logs.value.push({
    time,
    message,
    class: colorClass
  });
}

function clearLogs() {
  logs.value = [];
  movies.value = [];
  rawResponse.value = null;
  movieCount.value = 0;
}

async function testAPI() {
  clearLogs();
  addLog('🚀 开始API测试...', 'info');
  
  // 测试1: 直接使用axios测试
  addLog('测试1: 使用axios直接请求', 'info');
  try {
    const response = await axios.get('http://localhost:8000/api/v1/movies/');
    addLog(`✅ Axios请求成功! 状态码: ${response.status}`, 'success');
    addLog(`📊 返回数据类型: ${typeof response.data}`, 'info');
    
    if (response.data.count) {
      addLog(`🎬 电影总数: ${response.data.count}`, 'success');
      movieCount.value = response.data.count;
    }
    
    if (response.data.results && Array.isArray(response.data.results)) {
      addLog(`📝 当前页电影数: ${response.data.results.length}`, 'success');
      movies.value = response.data.results;
      rawResponse.value = JSON.stringify(response.data, null, 2);
    }
  } catch (error) {
    addLog(`❌ Axios请求失败: ${error.message}`, 'error');
    if (error.response) {
      addLog(`   状态码: ${error.response.status}`, 'error');
      addLog(`   响应: ${JSON.stringify(error.response.data)}`, 'error');
    } else if (error.request) {
      addLog(`   网络错误: 无法连接到服务器`, 'error');
      addLog(`   可能原因: CORS配置问题或后端未启动`, 'warning');
    }
  }
  
  // 测试2: 使用movieService
  addLog('', 'info');
  addLog('测试2: 使用movieService', 'info');
  try {
    const data = await movieService.getMovies();
    addLog(`✅ movieService请求成功!`, 'success');
    addLog(`📊 数据: ${JSON.stringify(data).substring(0, 100)}...`, 'info');
  } catch (error) {
    addLog(`❌ movieService请求失败: ${error.message}`, 'error');
  }
  
  // 测试3: 测试高分电影API
  addLog('', 'info');
  addLog('测试3: 测试高分电影API', 'info');
  try {
    const data = await movieService.getTopRatedMovies();
    if (Array.isArray(data)) {
      addLog(`✅ 高分电影API成功! 获取${data.length}部电影`, 'success');
      if (data.length > 0) {
        addLog(`   首部: ${data[0].title} (${data[0].douban_rating}分)`, 'success');
      }
    } else {
      addLog(`⚠️ 返回数据格式异常`, 'warning');
    }
  } catch (error) {
    addLog(`❌ 高分电影API失败: ${error.message}`, 'error');
  }
  
  addLog('', 'info');
  addLog('🏁 测试完成!', 'info');
}

function handleImageError(e) {
  e.target.src = 'https://via.placeholder.com/300x450?text=No+Image';
}

// 页面加载时自动测试
import { onMounted } from 'vue';
onMounted(() => {
  setTimeout(testAPI, 500);
});
</script>

<style scoped>
.debug-page {
  min-height: 100vh;
}
</style>
