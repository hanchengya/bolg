import api from './api';

export const adminService = {
  // 获取统计数据
  async getStats() {
    console.log('📞 [adminService.getStats] 开始请求...');
    try {
      const response = await api.get('/admin/stats/');
      console.log('📦 [adminService.getStats] 原始响应:', response);
      // api.js中已经返回了response.data，所以这里response就是我们需要的数据
      const data = response || {};
      console.log('✅ [adminService.getStats] 返回数据:', data);
      return data;
    } catch (error) {
      console.error('❌ [adminService.getStats] 请求失败:', error);
      return {
        totalUsers: 0,
        totalMovies: 0,
        totalRatings: 0,
        totalReviews: 0
      };
    }
  },

  // 用户管理
  async getUsers() {
    console.log('📞 [adminService.getUsers] 开始请求...');
    try {
      const response = await api.get('/admin/users/');
      console.log('📦 [adminService.getUsers] 原始响应:', response);
      // api.js中已经有response.data的处理，这里response就是data
      const data = Array.isArray(response) ? response : (response.data || []);
      console.log('✅ [adminService.getUsers] 返回数据:', data);
      return data;
    } catch (error) {
      console.error('❌ [adminService.getUsers] 请求失败:', error);
      throw error;
    }
  },

  async searchUsers(query) {
    const response = await api.get(`/admin/users/?search=${query}`);
    return response.data;
  },

  async createUser(userData) {
    const response = await api.post('/admin/users/', userData);
    return response.data;
  },

  async updateUser(userId, userData) {
    const response = await api.patch(`/admin/users/${userId}/`, userData);
    return response.data;
  },

  async deleteUser(userId) {
    const response = await api.delete(`/admin/users/${userId}/`);
    return response.data;
  },

  // 电影管理
  async getMovies() {
    console.log('📞 [adminService.getMovies] 开始请求...');
    try {
      const response = await api.get('/admin/movies/');
      console.log('📦 [adminService.getMovies] 原始响应:', response);
      const data = Array.isArray(response) ? response : (response.data || []);
      console.log('✅ [adminService.getMovies] 返回数据:', data.length, '部电影');
      return data;
    } catch (error) {
      console.error('❌ [adminService.getMovies] 请求失败:', error);
      throw error;
    }
  },

  async searchMovies(query) {
    console.log('📞 [adminService.searchMovies] 搜索:', query);
    try {
      const response = await api.get(`/admin/movies/?search=${query}`);
      const data = Array.isArray(response) ? response : (response.data || []);
      console.log('✅ [adminService.searchMovies] 找到', data.length, '部电影');
      return data;
    } catch (error) {
      console.error('❌ [adminService.searchMovies] 搜索失败:', error);
      throw error;
    }
  },

  async createMovie(movieData) {
    console.log('📤 [adminService.createMovie] 发送数据类型:', movieData.constructor.name);
    const response = await api.post('/admin/movies/', movieData);
    console.log('✅ [adminService.createMovie] 创建成功:', response);
    return response;
  },

  async updateMovie(movieId, movieData) {
    console.log('📤 [adminService.updateMovie] 更新电影', movieId, '数据类型:', movieData.constructor.name);
    const response = await api.patch(`/admin/movies/${movieId}/`, movieData);
    console.log('✅ [adminService.updateMovie] 更新成功:', response);
    return response;
  },

  async deleteMovie(movieId) {
    const response = await api.delete(`/admin/movies/${movieId}/`);
    return response.data;
  },
};
