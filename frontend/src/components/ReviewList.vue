<template>
  <div class="review-list">
    <div v-if="reviews.length > 0" class="space-y-6">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="bg-bg-secondary rounded-lg p-6 hover:bg-bg-tertiary transition cursor-pointer"
        @click="goToReview(review.id)"
      >
        <!-- 头部 -->
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <h3 class="text-xl font-bold mb-2">{{ review.title }}</h3>
            <div class="flex items-center gap-4 text-sm text-gray-400">
              <span>{{ review.user.username }}</span>
              <span>{{ formatDate(review.created_at) }}</span>
              <span v-if="review.contains_spoilers" class="text-red-400">⚠️ 含剧透</span>
            </div>
          </div>
          
          <!-- 统计 -->
          <div class="flex items-center gap-4 text-sm">
            <span class="flex items-center gap-1">
              <span>👍</span>
              <span>{{ review.helpful_count }}</span>
            </span>
            <span class="flex items-center gap-1">
              <span>💬</span>
              <span>{{ review.comment_count }}</span>
            </span>
          </div>
        </div>

        <!-- 内容预览 -->
        <p class="text-gray-300 line-clamp-3">{{ review.content }}</p>

        <!-- 操作按钮（如果是自己的影评） -->
        <div v-if="userStore.user && review.user.id === userStore.user.id" class="mt-4 flex gap-3">
          <button
            @click.stop="$emit('edit', review)"
            class="text-sm text-blue-400 hover:text-blue-300 transition"
          >
            编辑
          </button>
          <button
            @click.stop="$emit('delete', review)"
            class="text-sm text-red-400 hover:text-red-300 transition"
          >
            删除
          </button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-12 text-gray-400">
      <p>还没有影评</p>
      <p class="text-sm mt-2">成为第一个发表影评的人吧！</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';

defineProps({
  reviews: {
    type: Array,
    default: () => [],
  },
});

defineEmits(['edit', 'delete']);

const router = useRouter();
const userStore = useUserStore();

const goToReview = (reviewId) => {
  router.push(`/reviews/${reviewId}`);
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
