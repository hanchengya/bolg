<template>
  <div class="movie-carousel relative rounded-lg overflow-hidden" style="height: 400px;">
    <!-- 轮播图主体 -->
    <div class="relative h-full">
      <TransitionGroup name="slide">
        <div
          v-for="(movie, index) in movies"
          :key="movie.id"
          v-show="index === currentIndex"
          class="absolute inset-0 w-full h-full"
        >
          <!-- 背景图片 - 优化显示 -->
          <div class="absolute inset-0 overflow-hidden">
            <!-- 模糊背景 -->
            <div 
              class="absolute inset-0 bg-cover bg-center scale-110 blur-xl opacity-40"
              :style="{ backgroundImage: `url(${movie.poster})` }"
            ></div>
            <!-- 清晰的海报（居右显示） -->
            <div 
              class="absolute right-0 top-0 bottom-0 w-1/3 bg-cover bg-center"
              :style="{ backgroundImage: `url(${movie.poster})` }"
            ></div>
            <!-- 渐变遮罩 -->
            <div class="absolute inset-0 bg-gradient-to-r from-black via-black/90 to-transparent"></div>
          </div>

          <!-- 内容 -->
          <div class="relative h-full flex items-center px-12">
            <div class="max-w-2xl">
              <div class="text-accent-primary text-sm font-semibold mb-2">
                评分 TOP {{ index + 1 }}
              </div>
              <h2 class="text-4xl font-bold mb-3 text-white drop-shadow-lg">
                {{ movie.title }}
              </h2>
              <div class="flex items-center gap-4 mb-4">
                <div class="flex items-center">
                  <span class="text-yellow-400 text-2xl font-bold">{{ movie.douban_rating }}</span>
                  <span class="text-gray-400 ml-1">分</span>
                </div>
                <span class="text-gray-300">{{ movie.year }}</span>
                <span class="text-gray-300">{{ movie.genres }}</span>
              </div>
              <div class="text-gray-300 mb-6 space-y-1">
                <p class="line-clamp-1"><span class="text-gray-400">导演：</span>{{ movie.director }}</p>
                <p class="line-clamp-1"><span class="text-gray-400">主演：</span>{{ movie.cast }}</p>
              </div>
              <router-link
                :to="`/movies/${movie.id}`"
                class="inline-block bg-accent-primary hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition"
              >
                查看详情
              </router-link>
            </div>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- 左右切换按钮 -->
    <button
      @click="prev"
      class="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition z-10"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <button
      @click="next"
      class="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition z-10"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>

    <!-- 指示器 -->
    <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-10">
      <button
        v-for="(movie, index) in movies"
        :key="`dot-${movie.id}`"
        @click="goTo(index)"
        class="w-2 h-2 rounded-full transition"
        :class="index === currentIndex ? 'bg-accent-primary w-8' : 'bg-white/50 hover:bg-white/80'"
      ></button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  movies: {
    type: Array,
    required: true,
    default: () => []
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  interval: {
    type: Number,
    default: 5000
  }
});

const currentIndex = ref(0);
let timer = null;

const next = () => {
  currentIndex.value = (currentIndex.value + 1) % props.movies.length;
};

const prev = () => {
  currentIndex.value = (currentIndex.value - 1 + props.movies.length) % props.movies.length;
};

const goTo = (index) => {
  currentIndex.value = index;
};

const startAutoplay = () => {
  if (props.autoplay && props.movies.length > 1) {
    timer = setInterval(next, props.interval);
  }
};

const stopAutoplay = () => {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
};

onMounted(() => {
  startAutoplay();
});

onUnmounted(() => {
  stopAutoplay();
});
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.6s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
