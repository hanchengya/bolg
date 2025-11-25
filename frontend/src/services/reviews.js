import api from './api';

export const reviewService = {
  // 获取影评列表
  getReviews(params = {}) {
    return api.get('/reviews/', { params });
  },

  // 获取某部电影的影评
  getMovieReviews(movieId) {
    return api.get('/reviews/', {
      params: { movie: movieId }
    });
  },

  // 获取某用户的影评
  getUserReviews(userId) {
    return api.get('/reviews/', {
      params: { user: userId }
    });
  },

  // 获取影评详情
  getReviewDetail(reviewId) {
    return api.get(`/reviews/${reviewId}/`);
  },

  // 发表影评
  createReview(data) {
    return api.post('/reviews/', data);
  },

  // 更新影评
  updateReview(reviewId, data) {
    return api.patch(`/reviews/${reviewId}/`, data);
  },

  // 删除影评
  deleteReview(reviewId) {
    return api.delete(`/reviews/${reviewId}/`);
  },

  // 标记影评有用
  markHelpful(reviewId) {
    return api.post(`/reviews/${reviewId}/helpful/`);
  },

  // 获取影评的评论
  getReviewComments(reviewId) {
    return api.get(`/reviews/${reviewId}/comments/`);
  },

  // 添加评论
  addComment(reviewId, content, parentId = null) {
    return api.post(`/reviews/${reviewId}/add_comment/`, {
      content: content,
      parent: parentId,
    });
  },
};
