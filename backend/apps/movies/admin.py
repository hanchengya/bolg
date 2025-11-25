from django.contrib import admin
from .models import Movie, Genre


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['rank', 'title', 'year', 'director', 'douban_rating', 'avg_rating', 'rating_count']
    list_filter = ['year', 'genres']
    search_fields = ['title', 'director', 'cast']
    ordering = ['rank']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
