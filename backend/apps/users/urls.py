from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserDetailView,
    change_password,
)

app_name = 'users'

urlpatterns = [
    # 认证相关
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    # 用户信息
    path('me/', UserProfileView.as_view(), name='profile'),
    path('change-password/', change_password, name='change-password'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
