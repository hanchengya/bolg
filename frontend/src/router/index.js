import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/movies',
    name: 'MovieList',
    component: () => import('../views/MovieList.vue'),
  },
  {
    path: '/movies/:id',
    name: 'MovieDetail',
    component: () => import('../views/MovieDetail.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/my-ratings',
    name: 'MyRatings',
    component: () => import('../views/MyRatings.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/my-watchlist',
    name: 'MyWatchlist',
    component: () => import('../views/MyWatchlist.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/write-review',
    name: 'WriteReview',
    component: () => import('../views/WriteReview.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reviews/:id',
    name: 'ReviewDetail',
    component: () => import('../views/ReviewDetail.vue'),
  },
  {
    path: '/reviews/:id/edit',
    name: 'EditReview',
    component: () => import('../views/WriteReview.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/search',
    name: 'SearchMovies',
    component: () => import('../views/SearchMovies.vue'),
  },
  {
    path: '/top-rated',
    name: 'TopRated',
    component: () => import('../views/TopRated.vue'),
  },
  {
    path: '/debug',
    name: 'DebugAPI',
    component: () => import('../views/DebugAPI.vue'),
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫 - 检查登录状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  
  // 如果路由需要认证但用户未登录，跳转到登录页
  if (to.meta.requiresAuth && !token) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }, // 保存目标路径，登录后可以跳转回去
    });
  } else {
    next();
  }
});

export default router;
