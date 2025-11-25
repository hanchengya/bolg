import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '../services/auth';

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null);
  const accessToken = ref(localStorage.getItem('access_token') || null);
  const refreshToken = ref(localStorage.getItem('refresh_token') || null);

  // 计算属性
  const isAuthenticated = computed(() => !!accessToken.value);
  const username = computed(() => user.value?.username || '');
  const userAvatar = computed(() => user.value?.avatar || null);
  const isAdmin = computed(() => user.value?.is_staff || false);

  // Actions
  async function login(credentials) {
    try {
      const data = await authService.login(credentials);
      
      // 保存tokens
      accessToken.value = data.access;
      refreshToken.value = data.refresh;
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);

      // 获取用户信息
      await fetchCurrentUser();
      
      return { success: true };
    } catch (error) {
      console.error('登录失败:', error);
      return { 
        success: false, 
        error: error.response?.data || '登录失败，请重试' 
      };
    }
  }

  async function register(userData) {
    try {
      const data = await authService.register(userData);
      
      // 注册成功后自动登录
      accessToken.value = data.access;
      refreshToken.value = data.refresh;
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      
      user.value = data.user;
      
      return { success: true };
    } catch (error) {
      console.error('注册失败:', error);
      return { 
        success: false, 
        error: error.response?.data || '注册失败，请重试' 
      };
    }
  }

  async function fetchCurrentUser() {
    try {
      const data = await authService.getCurrentUser();
      user.value = data;
      return { success: true };
    } catch (error) {
      console.error('获取用户信息失败:', error);
      // 如果Token过期，清除登录状态
      if (error.response?.status === 401) {
        logout();
      }
      return { success: false };
    }
  }

  async function updateProfile(userData) {
    try {
      const data = await authService.updateProfile(userData);
      user.value = data;
      return { success: true };
    } catch (error) {
      console.error('更新用户信息失败:', error);
      return { 
        success: false, 
        error: error.response?.data || '更新失败，请重试' 
      };
    }
  }

  function logout() {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // 初始化时如果有token，自动获取用户信息
  if (accessToken.value) {
    fetchCurrentUser();
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    username,
    userAvatar,
    isAdmin,
    login,
    register,
    logout,
    fetchCurrentUser,
    updateProfile,
  };
});
