import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class MovieChatService {
  /**
   * 发送消息给AI助手
   * @param {string} message - 用户消息
   * @returns {Promise<string>} AI回复
   */
  async sendMessage(message) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/movies/chat/`,
        { message },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 60000, // 60秒超时
        }
      );

      if (response.data.success) {
        return response.data.response;
      } else {
        throw new Error(response.data.error || '未知错误');
      }
    } catch (error) {
      console.error('发送消息失败:', error);
      
      if (error.code === 'ECONNABORTED') {
        throw new Error('请求超时，请重试');
      }
      
      if (error.response) {
        throw new Error(error.response.data.error || '服务器错误');
      }
      
      throw new Error('网络连接失败');
    }
  }

  /**
   * 获取电影推荐
   * @param {string} genre - 电影类型（可选）
   * @returns {Promise<string>} 推荐结果
   */
  async getRecommendation(genre = '') {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/movies/recommend/`,
        { genre },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 30000,
        }
      );

      if (response.data.success) {
        return response.data.recommendation;
      } else {
        throw new Error(response.data.error || '未知错误');
      }
    } catch (error) {
      console.error('获取推荐失败:', error);
      throw new Error('获取推荐失败');
    }
  }
}

export const movieChatService = new MovieChatService();
