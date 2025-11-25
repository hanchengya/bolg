<template>
  <div class="max-w-7xl mx-auto py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">🏆 高分电影榜</h1>
      <p class="text-gray-400">豆瓣评分 9.0 分以上的经典佳作</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-20">
      <div class="text-gray-400 text-xl">加载中...</div>
    </div>

    <!-- 电影列表 -->
    <div v-else-if="movies.length > 0">
      <!-- 统计信息 -->
      <div class="bg-bg-secondary rounded-lg p-6 mb-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <div>
            <div class="text-3xl font-bold text-accent-primary">{{ movies.length }}</div>
            <div class="text-gray-400 mt-2">高分电影</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-accent-primary">{{ averageRating }}</div>
            <div class="text-gray-400 mt-2">平均评分</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-accent-primary">{{ topRating }}</div>
            <div class="text-gray-400 mt-2">最高评分</div>
          </div>
        </div>
      </div>

      <!-- 排序选项 -->
      <div class="mb-6 flex items-center gap-4">
        <span class="text-gray-400">排序：</span>
        <button
          @click="sortBy = 'rating'"
          :class="sortBy === 'rating' ? 'text-accent-primary' : 'text-gray-400 hover:text-white'"
          class="transition"
        >
          评分从高到低
        </button>
        <button
          @click="sortBy = 'rank'"
          :class="sortBy === 'rank' ? 'text-accent-primary' : 'text-gray-400 hover:text-white'"
          class="transition"
        >
          排名从前到后
        </button>
        <button
          @click="sortBy = 'year'"
          :class="sortBy === 'year' ? 'text-accent-primary' : 'text-gray-400 hover:text-white'"
          class="transition"
        >
          年份从新到旧
        </button>
      </div>

      <!-- 电影卡片网格 -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
        <MovieCard
          v-for="movie in sortedMovies"
          :key="movie.id"
          :movie="movie"
        />
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-20">
      <div class="text-gray-400 text-xl">暂无高分电影</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { movieService } from '../services/movies';
import MovieCard from '../components/MovieCard.vue';

const movies = ref([]);
const loading = ref(true);
const sortBy = ref('rating'); // rating, rank, year

// 计算平均评分
const averageRating = computed(() => {
  if (movies.value.length === 0) return '0.0';
  const sum = movies.value.reduce((acc, m) => acc + parseFloat(m.douban_rating || 0), 0);
  return (sum / movies.value.length).toFixed(1);
});

// 最高评分
const topRating = computed(() => {
  if (movies.value.length === 0) return '0.0';
  const ratings = movies.value.map(m => parseFloat(m.douban_rating || 0));
  return Math.max(...ratings).toFixed(1);
});

// 排序后的电影列表
const sortedMovies = computed(() => {
  const list = [...movies.value];
  
  switch (sortBy.value) {
    case 'rating':
      return list.sort((a, b) => parseFloat(b.douban_rating || 0) - parseFloat(a.douban_rating || 0));
    case 'rank':
      return list.sort((a, b) => (a.rank || 999) - (b.rank || 999));
    case 'year':
      return list.sort((a, b) => (b.year || 0) - (a.year || 0));
    default:
      return list;
  }
});

// 获取高分电影
const fetchTopRatedMovies = async () => {
  loading.value = true;
  try {
    const data = await movieService.getTopRatedMovies();
    movies.value = data;
  } catch (error) {
    console.error('获取高分电影失败:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchTopRatedMovies();
});
</script>
