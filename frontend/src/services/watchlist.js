import api from './api';

export const watchlistService = {
  // 获取我的观影清单
  getMyWatchlist(status = null) {
    const params = status ? { status } : {};
    return api.get('/watchlist/', { params });
  },

  // 添加电影到清单
  addToWatchlist(movieId, status = 'want_to_watch') {
    return api.post('/watchlist/', {
      movie: movieId,
      status: status,
    });
  },

  // 更新清单状态
  updateWatchlistStatus(watchlistId, status) {
    return api.patch(`/watchlist/${watchlistId}/`, {
      status: status,
    });
  },

  // 从清单中移除
  removeFromWatchlist(watchlistId) {
    return api.delete(`/watchlist/${watchlistId}/`);
  },

  // 检查电影是否在清单中
  checkMovieInWatchlist(movieId) {
    return api.get('/watchlist/', {
      params: { movie: movieId }
    });
  },
};
