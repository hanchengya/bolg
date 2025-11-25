<template>
  <div class="movie-detail">
    <div v-if="loading" class="text-center py-20">
      <div class="text-gray-400 text-xl">加载中...</div>
    </div>

    <div v-else-if="movie" class="max-w-6xl mx-auto">
      <!-- 电影头部 -->
      <div class="bg-bg-secondary rounded-lg overflow-hidden mb-8">
        <div class="md:flex">
          <!-- 海报 -->
          <div class="md:w-1/3 select-none">
            <img
              :src="posterUrl"
              :alt="movie.title"
              class="w-full h-auto object-cover select-none pointer-events-none"
              @error="handleImageError"
              draggable="false"
            />
          </div>

          <!-- 电影信息 -->
          <div class="md:w-2/3 p-8">
            <h1 class="text-4xl font-bold mb-2">{{ movie.title }}</h1>
            <p class="text-gray-400 text-xl mb-4">{{ movie.original_title }}</p>

            <div class="flex items-center mb-6">
              <div class="flex items-center mr-6">
                <span class="text-accent-primary text-3xl mr-2">★</span>
                <span class="text-3xl font-bold">{{ movie.douban_rating }}</span>
                <span class="text-gray-400 ml-2">豆瓣评分</span>
              </div>
              <div class="text-gray-400">
                排名: #{{ movie.rank }}
              </div>
            </div>

            <div class="space-y-3 text-gray-300">
              <div><span class="text-gray-500">导演:</span> {{ movie.director || '未知' }}</div>
              <div><span class="text-gray-500">主演:</span> {{ formatCast(movie.cast_list) || '未知' }}</div>
              <div><span class="text-gray-500">类型:</span> {{ formatGenres(movie.genres_list) || '未分类' }}</div>
              <div><span class="text-gray-500">年份:</span> {{ movie.year || '未知' }}</div>
              <div><span class="text-gray-500">国家:</span> {{ movie.country || '未知' }}</div>
              <div v-if="movie.runtime"><span class="text-gray-500">时长:</span> {{ movie.runtime }} 分钟</div>
            </div>

            <div class="mt-8 flex gap-4">
              <a
                v-if="movie.douban_url"
                :href="movie.douban_url"
                target="_blank"
                class="bg-accent-secondary hover:bg-red-700 text-white px-6 py-3 rounded-lg inline-block transition"
              >
                在豆瓣上查看
              </a>
              
              <!-- 添加到观影清单 -->
              <WatchlistButton
                :movie-id="movie.id"
                @added="handleWatchlistAdded"
                @removed="handleWatchlistRemoved"
                @statusChanged="handleWatchlistStatusChanged"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 我的评分 -->
      <div class="bg-bg-secondary rounded-lg p-8 mb-8">
        <h2 class="text-2xl font-bold mb-4">我的评分</h2>
        <RatingWidget
          :movie-id="movie.id"
          :initial-rating="myRating?.score ? Number(myRating.score) : 0"
          :rating-id="myRating?.id || null"
          @rated="handleRated"
          @deleted="handleRatingDeleted"
        />
      </div>

      <!-- 剧情简介 -->
      <div class="bg-bg-secondary rounded-lg p-8 mb-8">
        <h2 class="text-2xl font-bold mb-4">剧情简介</h2>
        <p class="text-gray-300 leading-relaxed">
          {{ movie.summary || '暂无剧情简介' }}
        </p>
      </div>

      <!-- 影评区 -->
      <div class="bg-bg-secondary rounded-lg p-8 mb-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold">影评</h2>
          <router-link
            v-if="userStore.isAuthenticated"
            :to="`/write-review?movieId=${movie.id}`"
            class="px-6 py-2 bg-accent-primary hover:bg-red-700 text-white rounded-lg transition"
          >
            写影评
          </router-link>
          <router-link
            v-else
            to="/login"
            class="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition"
          >
            登录后写影评
          </router-link>
        </div>

        <ReviewList
          :reviews="movieReviews"
          @delete="handleDeleteReview"
        />
      </div>

      <!-- 返回按钮 -->
      <div class="text-center">
        <button
          @click="$router.back()"
          class="bg-bg-secondary hover:bg-bg-tertiary text-white px-8 py-3 rounded-lg transition"
        >
          返回列表
        </button>
      </div>
    </div>

    <div v-else class="text-center py-20">
      <div class="text-gray-400 text-xl">电影不存在</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { movieService } from '../services/movies';
import { ratingService } from '../services/ratings';
import { reviewService } from '../services/reviews';
import { useUserStore } from '../stores/user';
import RatingWidget from '../components/RatingWidget.vue';
import WatchlistButton from '../components/WatchlistButton.vue';
import ReviewList from '../components/ReviewList.vue';

const route = useRoute();
const userStore = useUserStore();
const movie = ref(null);
const myRating = ref(null);
const movieReviews = ref([]);
const loading = ref(true);

const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgZmlsbD0iIzMzMzMzMyIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7ml6DmtbfmiqU8L3RleHQ+PC9zdmc+';

const posterUrl = computed(() => {
  if (movie.value?.poster) {
    if (movie.value.poster.startsWith('http')) {
      return movie.value.poster;
    }
    return `http://localhost:8000/media/${movie.value.poster}`;
  }
  return placeholderImage;
});

const handleImageError = (e) => {
  e.target.src = placeholderImage;
};

const formatGenres = (genresList) => {
  if (Array.isArray(genresList)) {
    return genresList.join(' / ');
  }
  return genresList || '未分类';
};

const formatCast = (castList) => {
  if (Array.isArray(castList)) {
    return castList.join(' / ');
  }
  return castList || '未知';
};

// 获取用户对该电影的评分
const fetchMyRating = async () => {
  if (!userStore.isAuthenticated) return;
  
  try {
    const data = await ratingService.getMyRatings();
    // 处理分页数据：如果有results字段说明是分页数据，否则是数组
    const ratings = data.results || data;
    // 从我的评分列表中找到对应这部电影的评分
    myRating.value = ratings.find(r => r.movie === movie.value.id);
  } catch (error) {
    console.error('获取我的评分失败:', error);
  }
};

// 处理评分成功
const handleRated = (ratingData) => {
  myRating.value = ratingData;
  console.log('评分成功:', ratingData);
};

// 处理删除评分
const handleRatingDeleted = () => {
  myRating.value = null;
  console.log('评分已删除');
};

// 处理添加到观影清单
const handleWatchlistAdded = (data) => {
  console.log('已添加到观影清单:', data);
};

// 处理从观影清单移除
const handleWatchlistRemoved = () => {
  console.log('已从观影清单移除');
};

// 处理观影清单状态变化
const handleWatchlistStatusChanged = (data) => {
  console.log('观影清单状态已更新:', data);
};

// 获取电影的影评
const fetchMovieReviews = async () => {
  try {
    const data = await reviewService.getMovieReviews(movie.value.id);
    movieReviews.value = data.results || data;
  } catch (error) {
    console.error('获取影评失败:', error);
  }
};

// 删除影评
const handleDeleteReview = async (review) => {
  if (!confirm('确定要删除这篇影评吗？')) return;

  try {
    await reviewService.deleteReview(review.id);
    movieReviews.value = movieReviews.value.filter(r => r.id !== review.id);
  } catch (error) {
    console.error('删除影评失败:', error);
    alert('删除失败，请重试');
  }
};

onMounted(async () => {
  try {
    const data = await movieService.getMovieDetail(route.params.id);
    movie.value = data;
    
    // 如果用户已登录，获取用户评分
    if (userStore.isAuthenticated) {
      await fetchMyRating();
    }

    // 获取影评
    await fetchMovieReviews();
  } catch (error) {
    console.error('获取电影详情失败:', error);
  } finally {
    loading.value = false;
  }
});
</script>
