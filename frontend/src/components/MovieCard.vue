<template>
  <div class="movie-card group" @click="goToDetail">
    <div class="relative overflow-hidden">
      <img
        :src="posterUrl"
        :alt="movie.title"
        :title="movie.title"
        class="w-full h-auto object-cover transition-transform group-hover:scale-110"
        @error="handleImageError"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
        <div class="absolute bottom-0 left-0 right-0 p-4">
          <h4 class="text-lg font-bold mb-2">{{ movie.title }}</h4>
          <div class="text-sm text-gray-300 space-y-1">
            <p v-if="movie.director">导演: {{ movie.director }}</p>
            <p v-if="movie.cast || movie.cast_list">主演: {{ formatCast(movie.cast_list || movie.cast) }}</p>
            <p v-if="movie.year || movie.country">
              {{ movie.year || '' }}{{ movie.year && movie.country ? ' · ' : '' }}{{ movie.country || '' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="p-4">
      <h3 class="text-lg font-semibold mb-2 line-clamp-1" :title="movie.title">
        {{ movie.title }}
      </h3>

      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center">
          <span class="text-accent-primary text-xl mr-1">★</span>
          <span class="text-white font-bold">{{ movie.douban_rating || 'N/A' }}</span>
        </div>
        <span class="text-gray-400 text-sm">{{ movie.year || 'N/A' }}</span>
      </div>

      <div class="text-gray-400 text-sm line-clamp-1 mb-1">
        <span class="text-gray-500">国家：</span>{{ movie.country || '未知' }}
      </div>

      <div class="text-gray-400 text-sm line-clamp-1">
        <span class="text-gray-500">类型：</span>{{ formatGenres(movie.genres_list) || '未分类' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
});

const router = useRouter();

const formatGenres = (genresList) => {
  if (Array.isArray(genresList)) {
    return genresList.join(' / ');
  }
  return genresList || '未分类';
};

const formatCast = (castList) => {
  if (Array.isArray(castList)) {
    // 只显示前3个演员
    return castList.slice(0, 3).join(' / ');
  }
  if (typeof castList === 'string') {
    // 如果是字符串，尝试分割并取前3个
    const actors = castList.split('/').map(a => a.trim());
    return actors.slice(0, 3).join(' / ');
  }
  return castList || '';
};

const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgZmlsbD0iIzMzMzMzMyIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7ml6DmtbfmiqU8L3RleHQ+PC9zdmc+';

const posterUrl = computed(() => {
  if (props.movie.poster) {
    // 如果是完整URL，直接使用
    if (props.movie.poster.startsWith('http')) {
      return props.movie.poster;
    }
    // 如果是相对路径，添加后端服务器地址
    return `http://localhost:8000/media/${props.movie.poster}`;
  }
  return placeholderImage;
});

const handleImageError = (e) => {
  e.target.src = placeholderImage;
};

const goToDetail = () => {
  router.push(`/movies/${props.movie.id}`);
};
</script>
