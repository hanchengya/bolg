import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 30000, // 增加到30秒
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器 - 自动添加Token
api.interceptors.request.use(
  (config) => {
    console.log('📤 API请求:', config.url, '数据类型:', config.data?.constructor?.name);
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 如果是FormData，删除Content-Type让浏览器自动设置（包含boundary）
    if (config.data instanceof FormData) {
      console.log('📦 检测到FormData，让浏览器自动设置Content-Type');
      delete config.headers['Content-Type'];
    }
    
    return config;
  },
  (error) => {
    console.error('❌ 请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('✅ API响应成功:', response.config.url);
    return response.data;
  },
  (error) => {
    console.error('❌ API请求失败:', error.config?.url, error);
    if (error.response?.status === 401) {
      console.warn('⚠️ 401错误 - 需要认证');
      localStorage.removeItem('access_token');
      // 注释掉自动跳转，避免跳转到不存在的页面
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
