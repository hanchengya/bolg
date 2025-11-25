import api from './api';

export const authService = {
  // 用户注册
  register(userData) {
    return api.post('/auth/register/', userData);
  },

  // 用户登录
  login(credentials) {
    return api.post('/auth/login/', credentials);
  },

  // 刷新Token
  refreshToken(refreshToken) {
    return api.post('/auth/refresh/', { refresh: refreshToken });
  },

  // 获取当前用户信息
  getCurrentUser() {
    return api.get('/auth/me/');
  },

  // 更新用户信息
  updateProfile(userData) {
    return api.patch('/auth/me/', userData);
  },

  // 修改密码
  changePassword(passwordData) {
    return api.post('/auth/change-password/', passwordData);
  },

  // 获取指定用户信息
  getUserById(userId) {
    return api.get(`/auth/users/${userId}/`);
  },
};
