<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-bg-secondary p-8 rounded-lg shadow-lg">
      <div>
        <h2 class="text-center text-3xl font-bold text-white mb-2">
          用户注册
        </h2>
        <p class="text-center text-gray-400 mb-8">
          创建账号，加入电影社区
        </p>
      </div>

      <form class="space-y-6" @submit.prevent="handleRegister">
        <!-- 错误提示 -->
        <div v-if="errorMessage" class="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded">
          <div v-if="typeof errorMessage === 'string'">{{ errorMessage }}</div>
          <ul v-else class="list-disc list-inside">
            <li v-for="(errors, field) in errorMessage" :key="field">
              <strong>{{ fieldLabels[field] || field }}:</strong> {{ Array.isArray(errors) ? errors.join(', ') : errors }}
            </li>
          </ul>
        </div>

        <!-- 用户名 -->
        <div>
          <label for="username" class="block text-sm font-medium text-gray-300 mb-2">
            用户名 *
          </label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            required
            class="appearance-none relative block w-full px-3 py-2 border border-gray-700 bg-bg-tertiary placeholder-gray-500 text-white rounded-md focus:outline-none focus:ring-accent-primary focus:border-accent-primary sm:text-sm"
            placeholder="3-20个字符"
          />
        </div>

        <!-- 邮箱 -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
            邮箱 *
          </label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            required
            class="appearance-none relative block w-full px-3 py-2 border border-gray-700 bg-bg-tertiary placeholder-gray-500 text-white rounded-md focus:outline-none focus:ring-accent-primary focus:border-accent-primary sm:text-sm"
            placeholder="example@email.com"
          />
        </div>

        <!-- 密码 -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
            密码 *
          </label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            required
            class="appearance-none relative block w-full px-3 py-2 border border-gray-700 bg-bg-tertiary placeholder-gray-500 text-white rounded-md focus:outline-none focus:ring-accent-primary focus:border-accent-primary sm:text-sm"
            placeholder="至少8个字符"
          />
          <p class="mt-1 text-xs text-gray-500">密码需包含字母和数字</p>
        </div>

        <!-- 确认密码 -->
        <div>
          <label for="password_confirm" class="block text-sm font-medium text-gray-300 mb-2">
            确认密码 *
          </label>
          <input
            id="password_confirm"
            v-model="formData.password_confirm"
            type="password"
            required
            class="appearance-none relative block w-full px-3 py-2 border border-gray-700 bg-bg-tertiary placeholder-gray-500 text-white rounded-md focus:outline-none focus:ring-accent-primary focus:border-accent-primary sm:text-sm"
            placeholder="再次输入密码"
          />
        </div>

        <!-- 注册按钮 -->
        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-accent-primary hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">注册中...</span>
            <span v-else>注册</span>
          </button>
        </div>

        <!-- 登录链接 -->
        <div class="text-center">
          <span class="text-gray-400">已有账号？</span>
          <router-link to="/login" class="text-accent-primary hover:text-red-400 ml-1">
            立即登录
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
  email: '',
  password: '',
  password_confirm: '',
});

const loading = ref(false);
const errorMessage = ref('');

const fieldLabels = {
  username: '用户名',
  email: '邮箱',
  password: '密码',
  password_confirm: '确认密码',
};

const handleRegister = async () => {
  loading.value = true;
  errorMessage.value = '';

  const result = await userStore.register(formData.value);

  loading.value = false;

  if (result.success) {
    // 注册成功，跳转到首页
    router.push('/');
  } else {
    // 显示错误信息
    errorMessage.value = result.error || '注册失败，请重试';
  }
};
</script>
