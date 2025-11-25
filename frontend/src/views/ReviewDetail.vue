<template>
  <div class="max-w-4xl mx-auto py-8">
    <div v-if="loading" class="text-center py-20">
      <div class="text-gray-400 text-xl">加载中...</div>
    </div>

    <div v-else-if="review">
      <!-- 返回按钮 -->
      <button
        @click="$router.back()"
        class="mb-6 text-gray-400 hover:text-white transition flex items-center gap-2"
      >
        <span>←</span>
        <span>返回</span>
      </button>

      <!-- 影评内容 -->
      <div class="bg-bg-secondary rounded-lg p-8 mb-8">
        <!-- 头部 -->
        <div class="mb-6">
          <h1 class="text-3xl font-bold mb-4">{{ review.title }}</h1>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4 text-gray-400">
              <span>{{ review.user.username }}</span>
              <span>{{ formatDate(review.created_at) }}</span>
              <span v-if="review.contains_spoilers" class="text-red-400">⚠️ 含剧透</span>
            </div>
            
            <!-- 操作按钮 -->
            <div v-if="userStore.user && review.user.id === userStore.user.id" class="flex gap-3">
              <button
                @click="editReview"
                class="text-blue-400 hover:text-blue-300 transition"
              >
                编辑
              </button>
              <button
                @click="deleteReview"
                class="text-red-400 hover:text-red-300 transition"
              >
                删除
              </button>
            </div>
          </div>
        </div>

        <!-- 电影信息 -->
        <div v-if="review.movie" class="bg-bg-tertiary rounded-lg p-4 mb-6 flex items-center gap-4">
          <img
            :src="getMoviePoster(review.movie)"
            :alt="review.movie.title"
            class="w-20 h-auto rounded cursor-pointer"
            @click="goToMovie(review.movie.id)"
          />
          <div>
            <h3 class="text-lg font-bold cursor-pointer hover:text-accent-primary transition"
                @click="goToMovie(review.movie.id)">
              {{ review.movie.title }}
            </h3>
            <p class="text-gray-400 text-sm">{{ review.movie.original_title }}</p>
          </div>
        </div>

        <!-- 内容 -->
        <div class="text-gray-300 leading-relaxed whitespace-pre-wrap">
          {{ review.content }}
        </div>

        <!-- 互动 -->
        <div class="mt-8 flex items-center gap-6 pt-6 border-t border-gray-700">
          <button
            @click="markHelpful"
            :disabled="hasMarkedHelpful"
            class="flex items-center gap-2 px-4 py-2 bg-bg-tertiary hover:bg-gray-700 rounded-lg transition disabled:opacity-50"
          >
            <span>👍</span>
            <span>有用 ({{ review.helpful_count }})</span>
          </button>
          <div class="flex items-center gap-2 text-gray-400">
            <span>💬</span>
            <span>{{ review.comment_count }} 条评论</span>
          </div>
        </div>
      </div>

      <!-- 评论区（简化版） -->
      <div class="bg-bg-secondary rounded-lg p-8">
        <h2 class="text-2xl font-bold mb-6">评论</h2>
        <div class="text-center text-gray-400 py-8">
          评论功能即将推出
        </div>
      </div>
    </div>

    <div v-else class="text-center py-20">
      <div class="text-gray-400 text-xl">影评不存在</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { reviewService } from '../services/reviews';
import { useUserStore } from '../stores/user';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const review = ref(null);
const loading = ref(true);
const hasMarkedHelpful = ref(false);

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

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

const goToMovie = (movieId) => {
  router.push(`/movies/${movieId}`);
};

const editReview = () => {
  router.push(`/reviews/${review.value.id}/edit`);
};

const deleteReview = async () => {
  if (!confirm('确定要删除这篇影评吗？')) return;

  try {
    await reviewService.deleteReview(review.value.id);
    router.push(`/movies/${review.value.movie.id}`);
  } catch (error) {
    console.error('删除影评失败:', error);
    alert('删除失败，请重试');
  }
};

const markHelpful = async () => {
  if (!userStore.isAuthenticated) {
    alert('请先登录');
    return;
  }

  try {
    await reviewService.markHelpful(review.value.id);
    review.value.helpful_count++;
    hasMarkedHelpful.value = true;
  } catch (error) {
    console.error('标记失败:', error);
  }
};

onMounted(async () => {
  try {
    const data = await reviewService.getReviewDetail(route.params.id);
    review.value = data;
  } catch (error) {
    console.error('获取影评失败:', error);
  } finally {
    loading.value = false;
  }
});
</script>
