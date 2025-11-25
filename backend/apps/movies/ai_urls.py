"""
AI聊天专用URL配置
"""
from django.urls import path
from .views import movie_chat, movie_recommend, get_available_models, switch_model, get_current_model

app_name = 'ai_chat'

urlpatterns = [
    path('chat/', movie_chat, name='chat'),
    path('recommend/', movie_recommend, name='recommend'),
    path('models/', get_available_models, name='get_models'),
    path('models/switch/', switch_model, name='switch_model'),
    path('models/current/', get_current_model, name='current_model'),
]
