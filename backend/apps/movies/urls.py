from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet, movie_chat, movie_recommend

router = DefaultRouter()
router.register(r'', MovieViewSet, basename='movie')
router.register(r'genres', GenreViewSet, basename='genre')

app_name = 'movies'

urlpatterns = [
    path('chat/', movie_chat, name='movie-chat'),
    path('recommend/', movie_recommend, name='movie-recommend'),
] + router.urls
