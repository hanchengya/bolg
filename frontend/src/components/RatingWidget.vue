<template>
  <div class="rating-widget">
    <div class="flex items-center gap-4">
      <!-- 星星显示 -->
      <div class="flex items-center gap-1">
        <button
          v-for="star in 5"
          :key="star"
          @click="handleRating(star * 2)"
          @mouseenter="hoveredStar = star"
          @mouseleave="hoveredStar = 0"
          :disabled="!editable || loading"
          class="text-3xl transition-all duration-200 focus:outline-none disabled:cursor-not-allowed"
          :class="getStarClass(star)"
        >
          {{ getStarIcon(star) }}
        </button>
      </div>

      <!-- 评分数值 -->
      <div class="text-white text-lg font-medium">
        <span v-if="currentRating > 0">{{ currentRating.toFixed(1) }}</span>
        <span v-else class="text-gray-500">未评分</span>
      </div>
      <div v-if="currentRating > 0" class="text-gray-400 text-sm ml-2">
        ({{ getStarCount() }}星)
      </div>

      <!-- 删除评分按钮 -->
      <button
        v-if="editable && currentRating > 0 && !loading"
        @click="handleDelete"
        class="text-gray-400 hover:text-red-500 transition ml-2"
        title="删除评分"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-sm text-gray-400 mt-2">
      保存中...
    </div>

    <!-- 提示信息 -->
    <div v-if="message" class="text-sm mt-2" :class="messageType === 'success' ? 'text-green-400' : 'text-red-400'">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { ratingService } from '../services/ratings';
import { useUserStore } from '../stores/user';

const props = defineProps({
  movieId: {
    type: Number,
    required: true,
  },
  initialRating: {
    type: Number,
    default: 0,
  },
  ratingId: {
    type: Number,
    default: null,
  },
  editable: {
    type: Boolean,
    default: true,
  },
  size: {
    type: String,
    default: 'large', // large, medium, small
  },
});

const emit = defineEmits(['rated', 'deleted']);

const userStore = useUserStore();
const currentRating = ref(props.initialRating);
const hoveredStar = ref(0);
const loading = ref(false);
const message = ref('');
const messageType = ref('success');

// 监听初始评分变化
watch(() => props.initialRating, (newVal) => {
  currentRating.value = newVal;
});

// 获取星星样式（基于10分制，每星=2分）
const getStarClass = (star) => {
  const displayRating = hoveredStar.value || (currentRating.value / 2);
  const isActive = star <= displayRating;
  return {
    'text-yellow-400': isActive,
    'text-gray-600': !isActive,
    'hover:scale-110': props.editable && !loading,
    'cursor-pointer': props.editable && !loading,
  };
};

// 获取星星图标（基于10分制，每星=2分）
const getStarIcon = (star) => {
  const displayRating = hoveredStar.value || (currentRating.value / 2);
  if (star <= displayRating) {
    return '★'; // 实心星
  }
  return '☆'; // 空心星
};

// 获取星数
const getStarCount = () => {
  return (currentRating.value / 2).toFixed(1);
};

// 处理评分（接收10分制的分数：2, 4, 6, 8, 10）
const handleRating = async (score) => {
  if (!props.editable || loading.value) return;

  // 检查登录状态
  if (!userStore.isAuthenticated) {
    message.value = '请先登录后再评分';
    messageType.value = 'error';
    setTimeout(() => {
      message.value = '';
    }, 3000);
    return;
  }

  loading.value = true;
  message.value = '';

  try {
    let result;
    if (props.ratingId) {
      // 更新已有评分
      result = await ratingService.updateRating(props.ratingId, score);
    } else {
      // 新增评分
      result = await ratingService.rateMovie(props.movieId, score);
    }

    currentRating.value = score;
    message.value = `评分成功！${score}分 (${(score/2).toFixed(1)}星)`;
    messageType.value = 'success';
    
    emit('rated', result);

    setTimeout(() => {
      message.value = '';
    }, 2000);
  } catch (error) {
    console.error('评分失败:', error);
    message.value = error.response?.data?.detail || '评分失败，请重试';
    messageType.value = 'error';
    
    setTimeout(() => {
      message.value = '';
    }, 3000);
  } finally {
    loading.value = false;
  }
};

// 删除评分
const handleDelete = async () => {
  if (!props.ratingId || loading.value) return;

  if (!confirm('确定要删除评分吗？')) return;

  loading.value = true;
  message.value = '';

  try {
    await ratingService.deleteRating(props.ratingId);
    currentRating.value = 0;
    message.value = '评分已删除';
    messageType.value = 'success';
    
    emit('deleted');

    setTimeout(() => {
      message.value = '';
    }, 2000);
  } catch (error) {
    console.error('删除评分失败:', error);
    message.value = '删除失败，请重试';
    messageType.value = 'error';
    
    setTimeout(() => {
      message.value = '';
    }, 3000);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.rating-widget button:disabled {
  opacity: 0.6;
}
</style>
