<template>
  <div class="max-w-6xl mx-auto py-8">
    <h1 class="text-3xl font-bold mb-8">我的评分</h1>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-20">
      <div class="text-gray-400 text-xl">加载中...</div>
    </div>

    <!-- 评分列表 -->
    <div v-else-if="ratings.length > 0" class="space-y-4">
      <!-- 统计信息 -->
      <div class="bg-bg-secondary rounded-lg p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <div>
            <div class="text-3xl font-bold text-accent-primary">{{ ratings.length }}</div>
            <div class="text-gray-400 mt-2">已评分电影</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-accent-primary">{{ averageRating }}</div>
            <div class="text-gray-400 mt-2">平均评分</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-accent-primary">{{ highRatingsCount }}</div>
            <div class="text-gray-400 mt-2">高分推荐 (≥8分)</div>
          </div>
        </div>
      </div>

      <!-- 评分记录卡片 -->
      <div
        v-for="rating in sortedRatings"
        :key="rating.id"
        class="bg-bg-secondary rounded-lg p-6 hover:bg-bg-tertiary transition cursor-pointer"
        @click="goToMovie(rating.movie_detail.id)"
      >
        <div class="flex items-start gap-6">
          <!-- 电影海报 -->
          <div class="flex-shrink-0 w-24">
            <img
              :src="getMoviePoster(rating.movie_detail)"
              :alt="rating.movie_detail.title"
              class="w-full rounded shadow-lg"
            />
          </div>

          <!-- 电影信息和评分 -->
          <div class="flex-1">
            <div class="flex items-start justify-between">
              <div>
                <h3 class="text-xl font-bold mb-1">{{ rating.movie_detail.title }}</h3>
                <p class="text-gray-400 mb-2">{{ rating.movie_detail.original_title }}</p>
                <div class="flex items-center gap-4 text-sm text-gray-400">
                  <span>{{ rating.movie_detail.year }}</span>
                  <span>{{ formatGenres(rating.movie_detail.genres_list) }}</span>
                  <span>豆瓣: {{ rating.movie_detail.douban_rating }}</span>
                </div>
              </div>

              <!-- 我的评分 -->
              <div class="text-right">
                <div class="flex items-center gap-2">
                  <span class="text-yellow-400 text-2xl">{{ '★'.repeat(Math.floor(rating.score / 2)) }}</span>
                  <span v-if="(rating.score / 2) % 1 !== 0" class="text-yellow-400 text-2xl">☆</span>
                  <span class="text-white text-xl font-bold ml-2">{{ rating.score }}</span>
                </div>
                <div class="text-gray-500 text-sm mt-1">
                  {{ (rating.score / 2).toFixed(1) }}星 · {{ formatDate(rating.created_at) }}
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="mt-4 flex gap-3">
              <button
                @click.stop="editRating(rating)"
                class="text-sm text-blue-400 hover:text-blue-300 transition"
              >
                修改评分
              </button>
              <button
                @click.stop="deleteRating(rating)"
                class="text-sm text-red-400 hover:text-red-300 transition"
              >
                删除评分
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-20">
      <div class="text-gray-400 text-xl mb-4">还没有评分记录</div>
      <router-link
        to="/movies"
        class="inline-block bg-accent-primary hover:bg-red-700 text-white px-6 py-3 rounded-lg transition"
      >
        去评分电影
      </router-link>
    </div>

    <!-- 修改评分对话框 -->
    <div
      v-if="editingRating"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="cancelEdit"
    >
      <div class="bg-bg-secondary rounded-lg p-8 max-w-md w-full mx-4" @click.stop>
        <h3 class="text-2xl font-bold mb-4">修改评分</h3>
        <p class="text-gray-400 mb-6">{{ editingRating.movie_detail.title }}</p>
        
        <RatingWidget
          :movie-id="editingRating.movie_detail.id"
          :initial-rating="Number(editingRating.score)"
          :rating-id="editingRating.id"
          @rated="handleRatingUpdated"
        />

        <div class="mt-6 flex justify-end gap-3">
          <button
            @click="cancelEdit"
            class="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ratingService } from '../services/ratings';
import { useUserStore } from '../stores/user';
import RatingWidget from '../components/RatingWidget.vue';

const router = useRouter();
const userStore = useUserStore();

const ratings = ref([]);
const loading = ref(true);
const editingRating = ref(null);

const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgZmlsbD0iIzMzMzMzMyIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7ml6DmtbfmiqU8L3RleHQ+PC9zdmc+';

// 按评分时间倒序排列
const sortedRatings = computed(() => {
  return [...ratings.value].sort((a, b) => 
    new Date(b.created_at) - new Date(a.created_at)
  );
});

// 平均评分
const averageRating = computed(() => {
  if (ratings.value.length === 0) return '0.0';
  const sum = ratings.value.reduce((acc, r) => acc + parseFloat(r.score), 0);
  return (sum / ratings.value.length).toFixed(1);
});

// 10分好评数量（8分及以上）
const highRatingsCount = computed(() => {
  return ratings.value.filter(r => r.score >= 8).length;
});

// 获取电影海报
const getMoviePoster = (movie) => {
  if (movie.poster) {
    if (movie.poster.startsWith('http')) {
      return movie.poster;
    }
    return `http://localhost:8000/media/${movie.poster}`;
  }
  return placeholderImage;
};

// 格式化类型
const formatGenres = (genresList) => {
  if (Array.isArray(genresList)) {
    return genresList.slice(0, 2).join(' / ');
  }
  return genresList || '未分类';
};

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

// 跳转到电影详情
const goToMovie = (movieId) => {
  router.push(`/movies/${movieId}`);
};

// 编辑评分
const editRating = (rating) => {
  editingRating.value = rating;
};

// 取消编辑
const cancelEdit = () => {
  editingRating.value = null;
};

// 处理评分更新
const handleRatingUpdated = (newRating) => {
  const index = ratings.value.findIndex(r => r.id === newRating.id);
  if (index !== -1) {
    ratings.value[index] = newRating;
  }
  cancelEdit();
};

// 删除评分
const deleteRating = async (rating) => {
  if (!confirm(`确定要删除对《${rating.movie_detail.title}》的评分吗？`)) {
    return;
  }

  try {
    await ratingService.deleteRating(rating.id);
    ratings.value = ratings.value.filter(r => r.id !== rating.id);
  } catch (error) {
    console.error('删除评分失败:', error);
    alert('删除失败，请重试');
  }
};

// 获取评分列表
const fetchRatings = async () => {
  loading.value = true;
  try {
    const data = await ratingService.getMyRatings();
    // 处理分页数据：如果有results字段说明是分页数据，否则是数组
    ratings.value = data.results || data;
  } catch (error) {
    console.error('获取评分列表失败:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (!userStore.isAuthenticated) {
    router.push('/login');
    return;
  }
  fetchRatings();
});
</script>
