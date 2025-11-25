import api from './api';

export const movieService = {
  // 获取电影列表
  getMovies(params = {}) {
    return api.get('/movies/', { params });
  },

  // 获取电影详情
  getMovieDetail(id) {
    return api.get(`/movies/${id}/`);
  },

  // 搜索电影
  searchMovies(query) {
    return api.get('/movies/search/', { params: { q: query } });
  },

  // 获取高分电影
  getTopRatedMovies() {
    return api.get('/movies/top_rated/');
  },

  // 获取电影类型列表
  getGenres() {
    return api.get('/movies/genres/');
  },

  // 获取电影年份列表
  getYears() {
    return api.get('/movies/years/');
  },
};
