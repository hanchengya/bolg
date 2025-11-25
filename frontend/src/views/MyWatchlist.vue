<template>
  <div class="max-w-7xl mx-auto py-8">
    <h1 class="text-3xl font-bold mb-8">我的观影清单</h1>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-20">
      <div class="text-gray-400 text-xl">加载中...</div>
    </div>

    <!-- 观影清单内容 -->
    <div v-else-if="allWatchlist.length > 0">
      <!-- 统计信息 -->
      <div class="bg-bg-secondary rounded-lg p-6 mb-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
          <div>
            <div class="text-3xl font-bold text-accent-primary">{{ allWatchlist.length }}</div>
            <div class="text-gray-400 mt-2">总计</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-yellow-400">{{ wantToWatchCount }}</div>
            <div class="text-gray-400 mt-2">📌 想看</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-blue-400">{{ watchingCount }}</div>
            <div class="text-gray-400 mt-2">👀 在看</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-green-400">{{ watchedCount }}</div>
            <div class="text-gray-400 mt-2">✅ 已看</div>
          </div>
        </div>
      </div>

      <!-- 筛选标签 -->
      <div class="mb-6 flex items-center gap-4">
        <span class="text-gray-400">筛选：</span>
        <button
          @click="currentFilter = 'all'"
          :class="currentFilter === 'all' ? 'bg-accent-primary' : 'bg-bg-secondary hover:bg-bg-tertiary'"
          class="px-4 py-2 rounded-lg transition"
        >
          全部 ({{ allWatchlist.length }})
        </button>
        <button
          @click="currentFilter = 'want_to_watch'"
          :class="currentFilter === 'want_to_watch' ? 'bg-yellow-600' : 'bg-bg-secondary hover:bg-bg-tertiary'"
          class="px-4 py-2 rounded-lg transition"
        >
          📌 想看 ({{ wantToWatchCount }})
        </button>
        <button
          @click="currentFilter = 'watching'"
          :class="currentFilter === 'watching' ? 'bg-blue-600' : 'bg-bg-secondary hover:bg-bg-tertiary'"
          class="px-4 py-2 rounded-lg transition"
        >
          👀 在看 ({{ watchingCount }})
        </button>
        <button
          @click="currentFilter = 'watched'"
          :class="currentFilter === 'watched' ? 'bg-green-600' : 'bg-bg-secondary hover:bg-bg-tertiary'"
          class="px-4 py-2 rounded-lg transition"
        >
          ✅ 已看 ({{ watchedCount }})
        </button>
      </div>

      <!-- 电影列表 -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
        <div
          v-for="item in filteredWatchlist"
          :key="item.id"
          class="relative group cursor-pointer"
          @click="goToMovie(item.movie_detail.id)"
        >
          <!-- 电影卡片 -->
          <div class="bg-bg-secondary rounded-lg overflow-hidden shadow-lg hover:scale-105 transition">
            <img
              :src="getMoviePoster(item.movie_detail)"
              :alt="item.movie_detail.title"
              class="w-full h-auto"
            />
            <div class="p-4">
              <h3 class="font-bold text-white truncate">{{ item.movie_detail.title }}</h3>
              <div class="flex items-center justify-between mt-2">
                <span class="text-yellow-400">★ {{ item.movie_detail.douban_rating }}</span>
                <span class="text-gray-400 text-sm">{{ item.movie_detail.year }}</span>
              </div>
            </div>
          </div>

          <!-- 状态标签 -->
          <div class="absolute top-2 right-2 px-3 py-1 rounded-full text-sm font-medium"
               :class="getStatusBadgeClass(item.status)">
            {{ getStatusText(item.status) }}
          </div>

          <!-- 操作按钮 -->
          <div class="absolute inset-0 bg-black bg-opacity-70 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-3">
            <button
              @click.stop="changeStatus(item)"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
            >
              更改状态
            </button>
            <button
              @click.stop="removeItem(item)"
              class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition"
            >
              移除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-20">
      <div class="text-gray-400 text-xl mb-4">观影清单是空的</div>
      <p class="text-gray-500 mb-6">快去添加你想看的电影吧！</p>
      <router-link
        to="/movies"
        class="inline-block bg-accent-primary hover:bg-red-700 text-white px-6 py-3 rounded-lg transition"
      >
        浏览电影
      </router-link>
    </div>

    <!-- 更改状态对话框 -->
    <div
      v-if="editingItem"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="cancelEdit"
    >
      <div class="bg-bg-secondary rounded-lg p-8 max-w-md w-full mx-4" @click.stop>
        <h3 class="text-2xl font-bold mb-4">更改状态</h3>
        <p class="text-gray-400 mb-6">{{ editingItem.movie_detail.title }}</p>
        
        <div class="space-y-3 mb-6">
          <button
            @click="updateStatus('want_to_watch')"
            class="w-full px-4 py-3 text-left bg-yellow-600 hover:bg-yellow-700 rounded-lg transition flex items-center gap-3"
          >
            <span class="text-2xl">📌</span>
            <span>想看</span>
          </button>
          <button
            @click="updateStatus('watching')"
            class="w-full px-4 py-3 text-left bg-blue-600 hover:bg-blue-700 rounded-lg transition flex items-center gap-3"
          >
            <span class="text-2xl">👀</span>
            <span>在看</span>
          </button>
          <button
            @click="updateStatus('watched')"
            class="w-full px-4 py-3 text-left bg-green-600 hover:bg-green-700 rounded-lg transition flex items-center gap-3"
          >
            <span class="text-2xl">✅</span>
            <span>已看</span>
          </button>
        </div>

        <button
          @click="cancelEdit"
          class="w-full px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition"
        >
          取消
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { watchlistService } from '../services/watchlist';
import { useUserStore } from '../stores/user';

const router = useRouter();
const userStore = useUserStore();

const allWatchlist = ref([]);
const loading = ref(true);
const currentFilter = ref('all');
const editingItem = ref(null);

const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgZmlsbD0iIzMzMzMzMyIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7ml6DmtbfmiqU8L3RleHQ+PC9zdmc+';

// 统计数量
const wantToWatchCount = computed(() => 
  allWatchlist.value.filter(item => item.status === 'want_to_watch').length
);

const watchingCount = computed(() => 
  allWatchlist.value.filter(item => item.status === 'watching').length
);

const watchedCount = computed(() => 
  allWatchlist.value.filter(item => item.status === 'watched').length
);

// 筛选后的清单
const filteredWatchlist = computed(() => {
  if (currentFilter.value === 'all') {
    return allWatchlist.value;
  }
  return allWatchlist.value.filter(item => item.status === currentFilter.value);
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

// 获取状态文字
const getStatusText = (status) => {
  const statusMap = {
    'want_to_watch': '想看',
    'watching': '在看',
    'watched': '已看'
  };
  return statusMap[status] || status;
};

// 获取状态标签样式
const getStatusBadgeClass = (status) => {
  const classMap = {
    'want_to_watch': 'bg-yellow-600',
    'watching': 'bg-blue-600',
    'watched': 'bg-green-600'
  };
  return classMap[status] || 'bg-gray-600';
};

// 跳转到电影详情
const goToMovie = (movieId) => {
  router.push(`/movies/${movieId}`);
};

// 打开更改状态对话框
const changeStatus = (item) => {
  editingItem.value = item;
};

// 取消编辑
const cancelEdit = () => {
  editingItem.value = null;
};

// 更新状态
const updateStatus = async (newStatus) => {
  if (!editingItem.value) return;

  try {
    await watchlistService.updateWatchlistStatus(editingItem.value.id, newStatus);
    editingItem.value.status = newStatus;
    cancelEdit();
  } catch (error) {
    console.error('更新状态失败:', error);
    alert('更新失败，请重试');
  }
};

// 移除项目
const removeItem = async (item) => {
  if (!confirm(`确定要从清单中移除《${item.movie_detail.title}》吗？`)) {
    return;
  }

  try {
    await watchlistService.removeFromWatchlist(item.id);
    allWatchlist.value = allWatchlist.value.filter(w => w.id !== item.id);
  } catch (error) {
    console.error('移除失败:', error);
    alert('移除失败，请重试');
  }
};

// 获取观影清单
const fetchWatchlist = async () => {
  loading.value = true;
  try {
    const data = await watchlistService.getMyWatchlist();
    allWatchlist.value = data.results || data;
  } catch (error) {
    console.error('获取观影清单失败:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (!userStore.isAuthenticated) {
    router.push('/login');
    return;
  }
  fetchWatchlist();
});
</script>
