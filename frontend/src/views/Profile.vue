<template>
  <div class="max-w-4xl mx-auto py-8">
    <div v-if="loading" class="text-center py-20">
      <div class="text-gray-400 text-xl">加载中...</div>
    </div>

    <div v-else-if="userStore.user" class="space-y-6">
      <!-- 用户信息卡片 -->
      <div class="bg-bg-secondary rounded-lg p-6">
        <h2 class="text-2xl font-bold mb-6">个人资料</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- 用户名 -->
          <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">用户名</label>
            <div class="text-white text-lg">{{ userStore.user.username }}</div>
          </div>

          <!-- 邮箱 -->
          <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">邮箱</label>
            <div class="text-white text-lg">{{ userStore.user.email }}</div>
          </div>

          <!-- 注册时间 -->
          <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">注册时间</label>
            <div class="text-white">{{ formatDate(userStore.user.date_joined) }}</div>
          </div>

          <!-- 统计信息 -->
          <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">社交统计</label>
            <div class="flex gap-4 text-white">
              <span>粉丝: {{ userStore.user.follower_count }}</span>
              <span>关注: {{ userStore.user.following_count }}</span>
            </div>
          </div>
        </div>

        <!-- 个人简介 -->
        <div class="mt-6">
          <label class="block text-sm font-medium text-gray-400 mb-2">个人简介</label>
          <div v-if="!editing" class="text-white">
            {{ userStore.user.bio || '暂无简介' }}
          </div>
          <textarea
            v-else
            v-model="editForm.bio"
            rows="3"
            class="w-full px-3 py-2 bg-bg-tertiary border border-gray-700 rounded-md text-white focus:outline-none focus:ring-accent-primary focus:border-accent-primary"
            placeholder="介绍一下自己吧..."
          ></textarea>
        </div>

        <!-- 所在地 -->
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-400 mb-2">所在地</label>
          <div v-if="!editing" class="text-white">
            {{ userStore.user.location || '未设置' }}
          </div>
          <input
            v-else
            v-model="editForm.location"
            type="text"
            class="w-full px-3 py-2 bg-bg-tertiary border border-gray-700 rounded-md text-white focus:outline-none focus:ring-accent-primary focus:border-accent-primary"
            placeholder="如：北京"
          />
        </div>

        <!-- 个人网站 -->
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-400 mb-2">个人网站</label>
          <div v-if="!editing" class="text-white">
            <a v-if="userStore.user.website" :href="userStore.user.website" target="_blank" class="text-accent-primary hover:underline">
              {{ userStore.user.website }}
            </a>
            <span v-else>未设置</span>
          </div>
          <input
            v-else
            v-model="editForm.website"
            type="url"
            class="w-full px-3 py-2 bg-bg-tertiary border border-gray-700 rounded-md text-white focus:outline-none focus:ring-accent-primary focus:border-accent-primary"
            placeholder="https://example.com"
          />
        </div>

        <!-- 操作按钮 -->
        <div class="mt-6 flex gap-4">
          <button
            v-if="!editing"
            @click="startEditing"
            class="px-6 py-2 bg-accent-primary hover:bg-red-700 text-white rounded-md transition"
          >
            编辑资料
          </button>
          <template v-else>
            <button
              @click="saveProfile"
              :disabled="saving"
              class="px-6 py-2 bg-accent-primary hover:bg-red-700 text-white rounded-md transition disabled:opacity-50"
            >
              {{ saving ? '保存中...' : '保存' }}
            </button>
            <button
              @click="cancelEditing"
              class="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition"
            >
              取消
            </button>
          </template>
        </div>

        <!-- 成功/错误提示 -->
        <div v-if="successMessage" class="mt-4 bg-green-900/50 border border-green-500 text-green-200 px-4 py-3 rounded">
          {{ successMessage }}
        </div>
        <div v-if="errorMessage" class="mt-4 bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded">
          {{ errorMessage }}
        </div>
      </div>

      <!-- 我的活动 -->
      <div class="bg-bg-secondary rounded-lg p-6 mb-6">
        <h3 class="text-xl font-bold mb-4">我的活动</h3>
        <div class="flex flex-wrap gap-3">
          <router-link
            to="/my-ratings"
            class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition inline-flex items-center gap-2"
          >
            <span>⭐</span>
            <span>我的评分</span>
          </router-link>
          <router-link
            to="/my-watchlist"
            class="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md transition inline-flex items-center gap-2"
          >
            <span>📋</span>
            <span>观影清单</span>
          </router-link>
          <button
            class="px-6 py-2 bg-gray-600 text-gray-400 rounded-md cursor-not-allowed"
            disabled
            title="即将推出"
          >
            我的影评（即将推出）
          </button>
        </div>
      </div>

      <!-- 退出登录 -->
      <div class="bg-bg-secondary rounded-lg p-6">
        <h3 class="text-xl font-bold mb-4">账户操作</h3>
        <button
          @click="handleLogout"
          class="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition"
        >
          退出登录
        </button>
      </div>
    </div>

    <div v-else class="text-center py-20">
      <div class="text-gray-400 text-xl">请先登录</div>
      <router-link to="/login" class="mt-4 inline-block text-accent-primary hover:underline">
        前往登录
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';

const router = useRouter();
const userStore = useUserStore();

const loading = ref(true);
const editing = ref(false);
const saving = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const editForm = ref({
  bio: '',
  location: '',
  website: '',
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

const startEditing = () => {
  editing.value = true;
  editForm.value = {
    bio: userStore.user.bio || '',
    location: userStore.user.location || '',
    website: userStore.user.website || '',
  };
  successMessage.value = '';
  errorMessage.value = '';
};

const cancelEditing = () => {
  editing.value = false;
  editForm.value = {
    bio: '',
    location: '',
    website: '',
  };
  errorMessage.value = '';
};

const saveProfile = async () => {
  saving.value = true;
  successMessage.value = '';
  errorMessage.value = '';

  const result = await userStore.updateProfile(editForm.value);

  saving.value = false;

  if (result.success) {
    editing.value = false;
    successMessage.value = '资料更新成功！';
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } else {
    errorMessage.value = typeof result.error === 'object' 
      ? Object.values(result.error).flat().join(', ')
      : result.error || '更新失败，请重试';
  }
};

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    userStore.logout();
    router.push('/');
  }
};

onMounted(async () => {
  if (userStore.isAuthenticated && !userStore.user) {
    await userStore.fetchCurrentUser();
  }
  loading.value = false;
});
</script>
