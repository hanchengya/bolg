import api from './api';

export const ratingService = {
  // 获取我的所有评分
  getMyRatings() {
    return api.get('/ratings/');
  },

  // 为电影评分
  rateMovie(movieId, score) {
    return api.post('/ratings/', {
      movie: movieId,
      score: score,
    });
  },

  // 更新评分
  updateRating(ratingId, score) {
    return api.patch(`/ratings/${ratingId}/`, {
      score: score,
    });
  },

  // 删除评分
  deleteRating(ratingId) {
    return api.delete(`/ratings/${ratingId}/`);
  },

  // 获取指定电影的我的评分
  getMyRatingForMovie(movieId) {
    return api.get('/ratings/', {
      params: { movie: movieId }
    });
  },
};
