from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-created_at']
