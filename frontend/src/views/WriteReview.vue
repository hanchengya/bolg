<template>
  <div class="max-w-4xl mx-auto py-8">
    <h1 class="text-3xl font-bold mb-8">{{ isEditing ? '编辑影评' : '发表影评' }}</h1>

    <!-- 电影信息 -->
    <div v-if="movie" class="bg-bg-secondary rounded-lg p-6 mb-8 flex items-center gap-4">
      <img
        :src="getMoviePoster(movie)"
        :alt="movie.title"
        class="w-24 h-auto rounded shadow-lg"
      />
      <div>
        <h2 class="text-2xl font-bold">{{ movie.title }}</h2>
        <p class="text-gray-400">{{ movie.original_title }}</p>
        <div class="text-sm text-gray-500 mt-2">
          {{ movie.year }} · {{ formatGenres(movie.genres_list) }}
        </div>
      </div>
    </div>

    <!-- 表单 -->
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- 标题 -->
      <div>
        <label class="block text-gray-300 mb-2">影评标题 *</label>
        <input
          v-model="formData.title"
          type="text"
          placeholder="给你的影评起个标题"
          class="w-full px-4 py-3 bg-bg-secondary border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-accent-primary"
          required
        />
      </div>

      <!-- 内容 -->
      <div>
        <label class="block text-gray-300 mb-2">影评内容 *</label>
        <textarea
          v-model="formData.content"
          rows="12"
          placeholder="写下你的观影感受..."
          class="w-full px-4 py-3 bg-bg-secondary border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-accent-primary resize-none"
          required
        ></textarea>
        <div class="text-sm text-gray-500 mt-2">
          已输入 {{ formData.content.length }} 字
        </div>
      </div>

      <!-- 剧透标记 -->
      <div class="flex items-center gap-3">
        <input
          v-model="formData.contains_spoilers"
          type="checkbox"
          id="spoilers"
          class="w-5 h-5"
        />
        <label for="spoilers" class="text-gray-300">
          ⚠️ 这篇影评包含剧透
        </label>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded">
        {{ error }}
      </div>

      <!-- 按钮 -->
      <div class="flex gap-4">
        <button
          type="submit"
          :disabled="loading"
          class="flex-1 px-6 py-3 bg-accent-primary hover:bg-red-700 text-white rounded-lg transition disabled:opacity-50"
        >
          {{ loading ? '发布中...' : (isEditing ? '更新影评' : '发表影评') }}
        </button>
        <button
          type="button"
          @click="handleCancel"
          class="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition"
        >
          取消
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { reviewService } from '../services/reviews';
import { movieService } from '../services/movies';
import { useUserStore } from '../stores/user';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const movie = ref(null);
const formData = ref({
  title: '',
  content: '',
  contains_spoilers: false,
});
const loading = ref(false);
const error = ref('');
const isEditing = ref(false);
const reviewId = ref(null);

const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgZmlsbD0iIzMzMzMzMyIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7ml6DmtbfmiqU8L3RleHQ+PC9zdmc+';

const getMoviePoster = (movie) => {
  if (movie.poster) {
    if (movie.poster.startsWith('http')) {
      return movie.poster;
    }
    return `http://localhost:8000/media/${movie.poster}`;
  }
  return placeholderImage;
};

const formatGenres = (genresList) => {
  if (Array.isArray(genresList)) {
    return genresList.slice(0, 3).join(' / ');
  }
  return genresList || '未分类';
};

const handleSubmit = async () => {
  if (!userStore.isAuthenticated) {
    error.value = '请先登录';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const data = {
      ...formData.value,
      movie: movie.value.id,
    };

    if (isEditing.value) {
      await reviewService.updateReview(reviewId.value, data);
    } else {
      await reviewService.createReview(data);
    }

    router.push(`/movies/${movie.value.id}`);
  } catch (err) {
    console.error('提交影评失败:', err);
    error.value = err.response?.data?.detail || '提交失败，请重试';
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  router.back();
};

onMounted(async () => {
  if (!userStore.isAuthenticated) {
    router.push('/login');
    return;
  }

  const movieId = route.params.movieId || route.query.movieId;
  reviewId.value = route.params.reviewId;

  if (reviewId.value) {
    // 编辑模式
    isEditing.value = true;
    try {
      const review = await reviewService.getReviewDetail(reviewId.value);
      formData.value = {
        title: review.title,
        content: review.content,
        contains_spoilers: review.contains_spoilers,
      };
      movie.value = review.movie;
    } catch (error) {
      console.error('获取影评失败:', error);
    }
  } else if (movieId) {
    // 新建模式
    try {
      movie.value = await movieService.getMovieDetail(movieId);
    } catch (error) {
      console.error('获取电影信息失败:', error);
    }
  }
});
</script>
