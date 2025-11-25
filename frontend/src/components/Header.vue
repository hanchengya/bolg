<template>
  <header class="bg-bg-secondary shadow-lg sticky top-0 z-50">
    <nav class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <router-link to="/" class="text-2xl font-bold text-accent-primary">
          🎬 电影博客
        </router-link>

        <div class="flex items-center space-x-4">
          <router-link to="/" class="text-gray-300 hover:text-white transition">
            首页
          </router-link>
          <router-link to="/movies" class="text-gray-300 hover:text-white transition">
            电影列表
          </router-link>
          <router-link to="/top-rated" class="text-gray-300 hover:text-white transition">
            高分榜单
          </router-link>
          <router-link to="/search" class="text-gray-300 hover:text-white transition">
            搜索
          </router-link>

          <!-- 用户已登录 -->
          <div v-if="userStore.isAuthenticated" class="flex items-center space-x-4 border-l border-gray-700 pl-4">
            <router-link to="/my-ratings" class="text-gray-300 hover:text-white transition">
              我的评分
            </router-link>
            <router-link to="/my-watchlist" class="text-gray-300 hover:text-white transition">
              观影清单
            </router-link>
            <!-- 管理员入口 -->
            <router-link
              v-if="userStore.isAdmin"
              to="/admin"
              class="text-accent-primary hover:text-red-400 transition font-semibold"
            >
              🔐 管理
            </router-link>
            <router-link to="/profile" class="flex items-center space-x-2 text-gray-300 hover:text-white transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span>{{ userStore.username }}</span>
            </router-link>
          </div>

          <!-- 用户未登录 -->
          <div v-else class="flex items-center space-x-4">
            <router-link to="/login" class="text-gray-300 hover:text-white transition">
              登录
            </router-link>
            <router-link to="/register" class="bg-accent-primary hover:bg-red-700 text-white px-4 py-2 rounded-md transition">
              注册
            </router-link>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useUserStore } from '../stores/user';

const userStore = useUserStore();
</script>
