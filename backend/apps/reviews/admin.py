from django.contrib import admin
from .models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'title', 'contains_spoilers', 'helpful_count', 'created_at']
    list_filter = ['contains_spoilers', 'created_at']
    search_fields = ['title', 'content', 'user__username', 'movie__title']
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']
    ordering = ['-created_at']
