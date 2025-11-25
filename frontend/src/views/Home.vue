<template>
  <div class="home">
    <!-- 评分前10电影轮播 -->
    <section class="hero-carousel mb-12">
      <div v-if="loading" class="bg-gradient-to-r from-bg-secondary to-bg-tertiary py-20 rounded-lg">
        <div class="text-center text-gray-400">加载中...</div>
      </div>
      <MovieCarousel v-else :movies="topTenMovies" :autoplay="true" :interval="5000" />
    </section>

    <!-- 影评广场 -->
    <section class="reviews-section bg-bg-secondary rounded-lg p-8 mb-12">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-3xl font-bold mb-2">📝 影评广场</h2>
          <p class="text-gray-400">阅读和发表影评</p>
        </div>
        <router-link
          to="/movies"
          class="text-accent-primary hover:text-red-400 transition font-semibold"
        >
          查看更多 →
        </router-link>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link
          to="/movies"
          class="bg-bg-tertiary p-6 rounded-lg hover:bg-gray-700 transition block"
        >
          <div class="text-4xl mb-4">✍️</div>
          <h3 class="text-xl font-bold mb-2">发表影评</h3>
          <p class="text-gray-400 mb-4">分享你对电影的独特见解</p>
          <span class="text-accent-primary hover:text-red-400 transition">
            开始写作 →
          </span>
        </router-link>
        <router-link
          to="/movies"
          class="bg-bg-tertiary p-6 rounded-lg hover:bg-gray-700 transition block"
        >
          <div class="text-4xl mb-4">💬</div>
          <h3 class="text-xl font-bold mb-2">热门讨论</h3>
          <p class="text-gray-400 mb-4">参与电影话题讨论</p>
          <span class="text-accent-primary hover:text-red-400 transition">
            加入讨论 →
          </span>
        </router-link>
        <router-link
          to="/movies"
          class="bg-bg-tertiary p-6 rounded-lg hover:bg-gray-700 transition block"
        >
          <div class="text-4xl mb-4">⭐</div>
          <h3 class="text-xl font-bold mb-2">精选影评</h3>
          <p class="text-gray-400 mb-4">阅读优质影评内容</p>
          <span class="text-accent-primary hover:text-red-400 transition">
            立即阅读 →
          </span>
        </router-link>
      </div>
    </section>

    <!-- 高分电影推荐 -->
    <section class="top-movies mb-12">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-3xl font-bold">🎯 高分电影推荐</h2>
        <router-link
          to="/top-rated"
          class="text-accent-primary hover:text-red-400 transition font-semibold"
        >
          查看全部 →
        </router-link>
      </div>
      
      <div v-if="loading" class="text-center py-12">
        <div class="text-gray-400">加载中...</div>
      </div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
        <MovieCard
          v-for="movie in displayMovies"
          :key="movie.id"
          :movie="movie"
        />
      </div>
    </section>

    <!-- 统计信息 -->
    <section class="stats bg-bg-secondary rounded-lg p-8">
      <h2 class="text-2xl font-bold mb-6 text-center">平台数据</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
        <div>
          <div class="text-3xl font-bold text-accent-primary">250</div>
          <div class="text-gray-400 mt-2">精选电影</div>
        </div>
        <div>
          <div class="text-3xl font-bold text-accent-primary">{{ topMoviesCount }}</div>
          <div class="text-gray-400 mt-2">高分佳作</div>
        </div>
        <div>
          <div class="text-3xl font-bold text-accent-primary" v-if="userStore.isAuthenticated">已登录</div>
          <div class="text-3xl font-bold text-gray-600" v-else>--</div>
          <div class="text-gray-400 mt-2">用户状态</div>
        </div>
        <div>
          <div class="text-3xl font-bold text-accent-primary">实时更新</div>
          <div class="text-gray-400 mt-2">数据状态</div>
        </div>
      </div>
    </section>

    <!-- AI聊天助手 -->
    <MovieChatBot />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { movieService } from '../services/movies';
import { useUserStore } from '../stores/user';
import MovieCard from '../components/MovieCard.vue';
import MovieCarousel from '../components/MovieCarousel.vue';
import MovieChatBot from '../components/MovieChatBot.vue';

const userStore = useUserStore();
const topMovies = ref([]);
const loading = ref(true);

// 轮播图显示前10部电影
const topTenMovies = computed(() => {
  return topMovies.value.slice(0, 10);
});

// 推荐区显示前10部电影（与轮播图相同）
const displayMovies = computed(() => {
  return topMovies.value.slice(0, 10);
});

// 高分电影数量
const topMoviesCount = computed(() => {
  return topMovies.value.length;
});

onMounted(async () => {
  try {
    const data = await movieService.getTopRatedMovies();
    topMovies.value = data;
  } catch (error) {
    console.error('获取电影失败:', error);
  } finally {
    loading.value = false;
  }
});
</script>
