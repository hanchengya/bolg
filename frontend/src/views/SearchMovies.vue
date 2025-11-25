<template>
  <div class="max-w-7xl mx-auto py-8">
    <h1 class="text-3xl font-bold mb-8">搜索电影</h1>

    <!-- 搜索框 - 独立渲染区域 -->
    <div class="mb-8" style="will-change: auto; contain: layout;">
      <div class="flex gap-4">
        <input
          :value="searchQuery"
          @input="searchQuery = $event.target.value"
          type="text"
          placeholder="搜索电影名称、导演、演员..."
          class="flex-1 px-4 py-3 bg-bg-secondary border-2 border-gray-700 rounded-lg text-white"
          style="outline: none !important; transition: none !important; border-color: #374151 !important; box-shadow: none !important; will-change: auto !important;"
          @keyup.enter="handleEnterKey"
          @compositionstart="isComposing = true"
          @compositionend="handleCompositionEnd"
          @blur="isComposing = false"
        />
        <button
          @click="handleSearch"
          :disabled="loading"
          class="px-8 py-3 bg-accent-primary hover:bg-red-700 text-white rounded-lg disabled:opacity-50"
          style="transition: opacity 0.2s;"
        >
          <span v-if="loading">搜索中...</span>
          <span v-else>搜索</span>
        </button>
      </div>
      
      <!-- 搜索提示 -->
      <p class="text-gray-400 text-sm mt-2">
        支持搜索：中文标题、英文标题、导演姓名、演员姓名
      </p>
    </div>

    <!-- 搜索结果 -->
    <div v-show="hasSearched">
      <!-- 加载状态 -->
      <div v-show="loading" class="text-center py-20">
        <div class="text-gray-400 text-xl">搜索中...</div>
      </div>

      <!-- 搜索结果 -->
      <div v-show="!loading && movies.length > 0">
        <div class="mb-6 text-gray-400">
          找到 <span class="text-white font-bold">{{ movies.length }}</span> 部电影
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <MovieCard
            v-for="movie in movies"
            :key="`movie-${movie.id}`"
            :movie="movie"
          />
        </div>
      </div>

      <!-- 无结果 -->
      <div v-show="!loading && hasSearched && movies.length === 0" class="text-center py-20">
        <div class="text-gray-400 text-xl mb-4">
          没有找到相关的电影
        </div>
        <p class="text-gray-500">
          试试其他关键词，或浏览全部电影
        </p>
        <router-link
          to="/movies"
          class="mt-6 inline-block bg-accent-primary hover:bg-red-700 text-white px-6 py-3 rounded-lg transition"
        >
          浏览全部电影
        </router-link>
      </div>
    </div>

    <!-- 初始状态 -->
    <div v-show="!hasSearched" class="text-center py-20">
      <div class="text-gray-400 text-xl mb-4">
        输入关键词开始搜索
      </div>
      <div class="text-gray-500">
        <p>🎬 搜索你喜欢的电影</p>
        <p class="mt-2">🎭 发现更多精彩内容</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { movieService } from '../services/movies';
import MovieCard from '../components/MovieCard.vue';

const route = useRoute();
const router = useRouter();

const searchQuery = ref(route.query.q?.toString() || '');
const movies = ref([]);
const loading = ref(false);
const hasSearched = ref(false);
const isComposing = ref(false);

// 处理Enter键
const handleEnterKey = () => {
  // 如果正在使用中文输入法，不执行搜索
  // keyup.enter + compositionend 的组合确保输入法完成后才触发
  if (isComposing.value) {
    return;
  }
  // 执行搜索
  handleSearch();
};

// 处理中文输入法结束
const handleCompositionEnd = () => {
  isComposing.value = false;
};

// 搜索电影
const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    return;
  }

  loading.value = true;
  hasSearched.value = true;

  try {
    const data = await movieService.searchMovies(searchQuery.value);
    movies.value = data;

    // 暂时移除URL更新，避免路由变化导致闪烁
    // router.replace({ query: { q: searchQuery.value } });
  } catch (error) {
    console.error('搜索失败:', error);
    movies.value = [];
  } finally {
    loading.value = false;
  }
};

// 初始化时不自动搜索，避免不必要的加载
// 用户需要手动点击搜索按钮或按Enter
</script>
