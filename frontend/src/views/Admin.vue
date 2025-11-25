<template>
  <div class="admin-panel">
    <h1 class="text-4xl font-bold mb-8">🔐 管理员控制台</h1>

    <!-- 统计卡片 -->
    <div v-if="statsLoading" class="text-center py-12">
      <div class="text-gray-400">加载统计数据中...</div>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-bg-secondary p-6 rounded-lg">
        <div class="text-gray-400 mb-2">总用户数</div>
        <div class="text-3xl font-bold text-accent-primary">{{ stats.totalUsers || 0 }}</div>
      </div>
      <div class="bg-bg-secondary p-6 rounded-lg">
        <div class="text-gray-400 mb-2">总电影数</div>
        <div class="text-3xl font-bold text-accent-primary">{{ stats.totalMovies || 0 }}</div>
      </div>
      <div class="bg-bg-secondary p-6 rounded-lg">
        <div class="text-gray-400 mb-2">总评分数</div>
        <div class="text-3xl font-bold text-accent-primary">{{ stats.totalRatings || 0 }}</div>
      </div>
      <div class="bg-bg-secondary p-6 rounded-lg">
        <div class="text-gray-400 mb-2">总影评数</div>
        <div class="text-3xl font-bold text-accent-primary">{{ stats.totalReviews || 0 }}</div>
      </div>
    </div>

    <!-- 导航标签 -->
    <div class="bg-bg-secondary rounded-lg mb-8">
      <div class="flex border-b border-gray-700">
        <button
          @click="activeTab = 'users'"
          class="px-6 py-4 font-semibold transition"
          :class="activeTab === 'users' ? 'text-accent-primary border-b-2 border-accent-primary' : 'text-gray-400 hover:text-white'"
        >
          👥 用户管理
        </button>
        <button
          @click="activeTab = 'movies'"
          class="px-6 py-4 font-semibold transition"
          :class="activeTab === 'movies' ? 'text-accent-primary border-b-2 border-accent-primary' : 'text-gray-400 hover:text-white'"
        >
          🎬 电影管理
        </button>
        <button
          @click="activeTab = 'ai'"
          class="px-6 py-4 font-semibold transition"
          :class="activeTab === 'ai' ? 'text-accent-primary border-b-2 border-accent-primary' : 'text-gray-400 hover:text-white'"
        >
          🤖 AI模型
        </button>
      </div>

      <!-- 内容区域 -->
      <div class="p-6">
        <div v-if="activeTab === 'users'">
          <AdminUsers v-if="!statsLoading" @stats-updated="loadStats" />
          <div v-else class="text-center py-12">
            <div class="text-gray-400">加载中...</div>
          </div>
        </div>
        <div v-if="activeTab === 'movies'">
          <AdminMovies v-if="!statsLoading" @stats-updated="loadStats" />
          <div v-else class="text-center py-12">
            <div class="text-gray-400">加载中...</div>
          </div>
        </div>
        <div v-if="activeTab === 'ai'">
          <AdminAIModels />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { adminService } from '../services/admin';
import AdminUsers from '../components/AdminUsers.vue';
import AdminMovies from '../components/AdminMovies.vue';
import AdminAIModels from '../components/AdminAIModels.vue';

const activeTab = ref('users');
const statsLoading = ref(true);
const stats = ref({
  totalUsers: 0,
  totalMovies: 0,
  totalRatings: 0,
  totalReviews: 0
});

const loadStats = async () => {
  statsLoading.value = true;
  try {
    const data = await adminService.getStats();
    console.log('Stats data:', data);
    if (data) {
      stats.value = {
        totalUsers: data.totalUsers || 0,
        totalMovies: data.totalMovies || 0,
        totalRatings: data.totalRatings || 0,
        totalReviews: data.totalReviews || 0
      };
    }
  } catch (error) {
    console.error('获取统计数据失败:', error);
    console.error('Error details:', error.response?.data || error.message);
    // 不显示alert，让用户仍然可以使用管理功能
  } finally {
    statsLoading.value = false;
  }
};

onMounted(() => {
  loadStats();
});
</script>
