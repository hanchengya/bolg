<template>
  <div class="watchlist-button">
    <!-- 已在清单中 -->
    <div v-if="inWatchlist" class="flex items-center gap-2">
      <select
        v-model="currentStatus"
        @change="handleStatusChange"
        :disabled="loading"
        class="px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-accent-primary disabled:opacity-50"
      >
        <option value="want_to_watch">想看</option>
        <option value="watching">在看</option>
        <option value="watched">已看</option>
      </select>
      
      <button
        @click="handleRemove"
        :disabled="loading"
        class="p-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition disabled:opacity-50"
        title="从清单移除"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- 未在清单中 -->
    <div v-else class="relative">
      <button
        @click="toggleDropdown"
        :disabled="loading || !userStore.isAuthenticated"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition disabled:opacity-50"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span v-if="loading">添加中...</span>
        <span v-else>加入清单</span>
      </button>

      <!-- 下拉菜单 -->
      <div
        v-if="showDropdown"
        class="absolute top-full left-0 mt-2 bg-bg-secondary border border-gray-700 rounded-lg shadow-lg overflow-hidden z-10 min-w-[150px]"
      >
        <button
          @click="handleAdd('want_to_watch')"
          class="w-full px-4 py-3 text-left hover:bg-bg-tertiary transition flex items-center gap-2"
        >
          <span>📌</span>
          <span>想看</span>
        </button>
        <button
          @click="handleAdd('watching')"
          class="w-full px-4 py-3 text-left hover:bg-bg-tertiary transition flex items-center gap-2"
        >
          <span>👀</span>
          <span>在看</span>
        </button>
        <button
          @click="handleAdd('watched')"
          class="w-full px-4 py-3 text-left hover:bg-bg-tertiary transition flex items-center gap-2"
        >
          <span>✅</span>
          <span>已看</span>
        </button>
      </div>
    </div>

    <!-- 提示信息 -->
    <div v-if="message" class="mt-2 text-sm" :class="messageType === 'success' ? 'text-green-400' : 'text-red-400'">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { watchlistService } from '../services/watchlist';
import { useUserStore } from '../stores/user';

const props = defineProps({
  movieId: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['added', 'removed', 'statusChanged']);

const userStore = useUserStore();
const inWatchlist = ref(false);
const watchlistId = ref(null);
const currentStatus = ref('want_to_watch');
const loading = ref(false);
const showDropdown = ref(false);
const message = ref('');
const messageType = ref('success');

// 检查电影是否在清单中
const checkWatchlist = async () => {
  if (!userStore.isAuthenticated) return;

  try {
    const data = await watchlistService.getMyWatchlist();
    const items = data.results || data;
    const item = items.find(w => w.movie === props.movieId);
    
    if (item) {
      inWatchlist.value = true;
      watchlistId.value = item.id;
      currentStatus.value = item.status;
    } else {
      inWatchlist.value = false;
      watchlistId.value = null;
    }
  } catch (error) {
    console.error('检查清单失败:', error);
  }
};

// 切换下拉菜单
const toggleDropdown = () => {
  if (!userStore.isAuthenticated) {
    message.value = '请先登录';
    messageType.value = 'error';
    setTimeout(() => {
      message.value = '';
    }, 2000);
    return;
  }
  showDropdown.value = !showDropdown.value;
};

// 添加到清单
const handleAdd = async (status) => {
  showDropdown.value = false;
  loading.value = true;
  message.value = '';

  try {
    const result = await watchlistService.addToWatchlist(props.movieId, status);
    inWatchlist.value = true;
    watchlistId.value = result.id;
    currentStatus.value = status;
    
    const statusText = {
      'want_to_watch': '想看',
      'watching': '在看',
      'watched': '已看'
    };
    
    message.value = `已添加到${statusText[status]}`;
    messageType.value = 'success';
    
    emit('added', result);

    setTimeout(() => {
      message.value = '';
    }, 2000);
  } catch (error) {
    console.error('添加到清单失败:', error);
    message.value = error.response?.data?.detail || '添加失败，请重试';
    messageType.value = 'error';
    
    setTimeout(() => {
      message.value = '';
    }, 3000);
  } finally {
    loading.value = false;
  }
};

// 更新状态
const handleStatusChange = async () => {
  loading.value = true;
  message.value = '';

  try {
    const result = await watchlistService.updateWatchlistStatus(watchlistId.value, currentStatus.value);
    
    const statusText = {
      'want_to_watch': '想看',
      'watching': '在看',
      'watched': '已看'
    };
    
    message.value = `已更新为${statusText[currentStatus.value]}`;
    messageType.value = 'success';
    
    emit('statusChanged', result);

    setTimeout(() => {
      message.value = '';
    }, 2000);
  } catch (error) {
    console.error('更新状态失败:', error);
    message.value = '更新失败，请重试';
    messageType.value = 'error';
    
    setTimeout(() => {
      message.value = '';
    }, 3000);
  } finally {
    loading.value = false;
  }
};

// 从清单移除
const handleRemove = async () => {
  if (!confirm('确定要从清单中移除吗？')) return;

  loading.value = true;
  message.value = '';

  try {
    await watchlistService.removeFromWatchlist(watchlistId.value);
    inWatchlist.value = false;
    watchlistId.value = null;
    
    message.value = '已从清单移除';
    messageType.value = 'success';
    
    emit('removed');

    setTimeout(() => {
      message.value = '';
    }, 2000);
  } catch (error) {
    console.error('移除失败:', error);
    message.value = '移除失败，请重试';
    messageType.value = 'error';
    
    setTimeout(() => {
      message.value = '';
    }, 3000);
  } finally {
    loading.value = false;
  }
};

// 点击外部关闭下拉菜单
const handleClickOutside = (event) => {
  if (!event.target.closest('.watchlist-button')) {
    showDropdown.value = false;
  }
};

onMounted(() => {
  checkWatchlist();
  document.addEventListener('click', handleClickOutside);
});

// 监听用户登录状态变化
watch(() => userStore.isAuthenticated, (newVal) => {
  if (newVal) {
    checkWatchlist();
  } else {
    inWatchlist.value = false;
    watchlistId.value = null;
  }
});
</script>
