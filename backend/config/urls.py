"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from apps.movies.admin_views import AdminStatsViewSet, AdminUserViewSet, AdminMovieViewSet

# 管理员路由
admin_router = DefaultRouter()
admin_router.register(r'stats', AdminStatsViewSet, basename='admin-stats')
admin_router.register(r'users', AdminUserViewSet, basename='admin-users')
admin_router.register(r'movies', AdminMovieViewSet, basename='admin-movies')

urlpatterns = [
    # 根路径重定向到API文档
    path('', RedirectView.as_view(url='/api/docs/', permanent=False), name='index'),

    path('admin/', admin.site.urls),

    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API endpoints
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/movies/', include('apps.movies.urls')),
    path('api/v1/reviews/', include('apps.reviews.urls')),
    path('api/v1/ratings/', include('apps.ratings.urls')),
    path('api/v1/watchlist/', include('apps.watchlists.urls')),
    
    # AI Chat API (without version prefix for simplicity)
    path('api/movies/', include('apps.movies.ai_urls')),
    
    # Admin API endpoints
    path('api/v1/admin/', include(admin_router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
