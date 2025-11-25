<template>
  <div class="movie-list">
    <h1 class="text-4xl font-bold mb-8">电影列表</h1>

    <!-- 搜索和筛选 -->
    <div class="mb-8 bg-bg-secondary p-6 rounded-lg">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <input
          v-model="searchQuery"
          @input="onSearchInput"
          @compositionstart="isComposing = true"
          @compositionend="handleCompositionEnd"
          type="text"
          placeholder="搜索电影..."
          class="px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
          style="transition: none !important;"
        />
        <select
          v-model="selectedGenre"
          @change="onFilterChange"
          class="px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
        >
          <option value="">全部类型</option>
          <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
        </select>
        <select
          v-model="selectedYear"
          @change="onFilterChange"
          class="px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
        >
          <option value="">全部年份</option>
          <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
        </select>
        <select
          v-model="ordering"
          @change="onFilterChange"
          class="px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
        >
          <option value="-douban_rating">评分从高到低</option>
          <option value="douban_rating">评分从低到高</option>
          <option value="rank">排名</option>
          <option value="-year">年份从新到旧</option>
        </select>
      </div>
    </div>

    <!-- 电影网格 -->
    <div class="relative min-h-[400px]">
      <!-- 加载遮罩 - 使用absolute定位避免布局抖动 -->
      <div v-if="loading" class="absolute inset-0 bg-bg-primary bg-opacity-80 flex items-center justify-center z-10">
        <div class="text-gray-400 text-xl">加载中...</div>
      </div>

      <!-- 电影列表 -->
      <div v-if="movies.length === 0 && !loading" class="text-center py-12">
        <div class="text-gray-400 text-xl">暂无电影数据</div>
      </div>
      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6" :class="{ 'opacity-50': loading }">
        <MovieCard
          v-for="movie in movies"
          :key="movie.id"
          :movie="movie"
        />
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="mt-12 flex justify-center">
      <div class="flex gap-2">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-4 py-2 bg-bg-secondary rounded-lg disabled:opacity-50"
        >
          上一页
        </button>
        <span class="px-4 py-2 bg-bg-tertiary rounded-lg">
          {{ currentPage }} / {{ totalPages }}
        </span>
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 bg-bg-secondary rounded-lg disabled:opacity-50"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { movieService } from '../services/movies';
import MovieCard from '../components/MovieCard.vue';

const movies = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const selectedGenre = ref('');
const selectedYear = ref('');
const ordering = ref('-douban_rating');
const currentPage = ref(1);
const totalPages = ref(1);
const genres = ref(['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '犯罪']);
const isComposing = ref(false);
const years = ref([]);
let searchTimeout = null;

// 从API获取年份列表
const loadYears = async () => {
  try {
    const yearList = await movieService.getYears();
    years.value = yearList;
  } catch (error) {
    console.error('获取年份列表失败:', error);
  }
};

const fetchMovies = async () => {
  console.log('🎬 MovieList.vue: 开始加载电影数据...');
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      ordering: ordering.value,
    };

    if (selectedGenre.value) params.genre = selectedGenre.value;
    if (selectedYear.value) params.year = selectedYear.value;

    console.log('📡 调用参数:', params);
    const data = await movieService.getMovies(params);
    console.log('✅ 获取数据成功:', data);
    console.log('📊 数据类型:', typeof data, '有 results:', !!data.results, '有 count:', data.count);
    
    movies.value = data.results || data;
    totalPages.value = Math.ceil((data.count || movies.value.length) / 20);
    console.log('🎬 设置 movies:', movies.value.length, '部电影, 总页数:', totalPages.value);
  } catch (error) {
    console.error('❌ 获取电影失败:', error);
    console.error('错误详情:', error.response || error.message);
  } finally {
    loading.value = false;
    console.log('✅ MovieList.vue: 加载完成');
  }
};

// 处理中文输入法结束
const handleCompositionEnd = () => {
  isComposing.value = false;
  // 输入法结束后立即触发搜索
  onSearchInput();
};

// 防抖搜索输入
const onSearchInput = () => {
  // 如果正在使用中文输入法，不执行搜索
  if (isComposing.value) {
    return;
  }

  // 清除之前的定时器
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }

  // 设置新的定时器，500ms后执行搜索
  searchTimeout = setTimeout(() => {
    onSearch();
  }, 500);
};

// 执行搜索
const onSearch = async () => {
  if (searchQuery.value.trim()) {
    loading.value = true;
    try {
      const data = await movieService.searchMovies(searchQuery.value);
      movies.value = data.results || data;
      totalPages.value = 1; // 搜索结果不分页
    } catch (error) {
      console.error('搜索失败:', error);
      movies.value = [];
    } finally {
      loading.value = false;
    }
  } else {
    // 搜索框为空时，恢复正常列表
    fetchMovies();
  }
};

const onFilterChange = () => {
  currentPage.value = 1;
  fetchMovies();
};

const goToPage = (page) => {
  currentPage.value = page;
  fetchMovies();
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

onMounted(() => {
  loadYears();
  fetchMovies();
});
</script>
