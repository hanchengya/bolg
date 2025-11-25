from django.contrib import admin
from .models import Watchlist


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'status', 'added_at']
    list_filter = ['status', 'added_at']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-added_at']
