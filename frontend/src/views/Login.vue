<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-bg-secondary p-8 rounded-lg shadow-lg">
      <div>
        <h2 class="text-center text-3xl font-bold text-white mb-2">
          用户登录
        </h2>
        <p class="text-center text-gray-400 mb-8">
          登录后可以发表评论和评分
        </p>
      </div>

      <form class="space-y-6" @submit.prevent="handleLogin">
        <!-- 错误提示 -->
        <div v-if="errorMessage" class="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded">
          {{ errorMessage }}
        </div>

        <!-- 用户名 -->
        <div>
          <label for="username" class="block text-sm font-medium text-gray-300 mb-2">
            用户名
          </label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            required
            class="appearance-none relative block w-full px-3 py-2 border border-gray-700 bg-bg-tertiary placeholder-gray-500 text-white rounded-md focus:outline-none focus:ring-accent-primary focus:border-accent-primary focus:z-10 sm:text-sm"
            placeholder="请输入用户名"
          />
        </div>

        <!-- 密码 -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
            密码
          </label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            required
            class="appearance-none relative block w-full px-3 py-2 border border-gray-700 bg-bg-tertiary placeholder-gray-500 text-white rounded-md focus:outline-none focus:ring-accent-primary focus:border-accent-primary focus:z-10 sm:text-sm"
            placeholder="请输入密码"
          />
        </div>

        <!-- 登录按钮 -->
        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-accent-primary hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">登录中...</span>
            <span v-else>登录</span>
          </button>
        </div>

        <!-- 注册链接 -->
        <div class="text-center">
          <span class="text-gray-400">还没有账号？</span>
          <router-link to="/register" class="text-accent-primary hover:text-red-400 ml-1">
            立即注册
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';

const router = useRouter();
const userStore = useUserStore();

const formData = ref({
  username: '',
  password: '',
});

const loading = ref(false);
const errorMessage = ref('');

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = '';

  const result = await userStore.login(formData.value);

  loading.value = false;

  if (result.success) {
    // 登录成功，跳转到目标页面或首页
    const redirect = router.currentRoute.value.query.redirect || '/';
    router.push(redirect);
  } else {
    // 显示错误信息
    if (typeof result.error === 'object') {
      errorMessage.value = Object.values(result.error).flat().join(', ');
    } else {
      errorMessage.value = result.error || '登录失败，请检查用户名和密码';
    }
  }
};
</script>
