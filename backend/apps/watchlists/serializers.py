from rest_framework import serializers
from .models import Watchlist
from apps.movies.serializers import MovieListSerializer


class WatchlistSerializer(serializers.ModelSerializer):
    """观影清单序列化器"""
    movie_detail = MovieListSerializer(source='movie', read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'movie_detail', 'status', 'added_at', 'watched_at']
        read_only_fields = ['id', 'movie_detail', 'added_at']


class WatchlistCreateSerializer(serializers.ModelSerializer):
    """观影清单创建序列化器"""

    class Meta:
        model = Watchlist
        fields = ['movie', 'status']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # 使用update_or_create来处理状态的更新
        watchlist, created = Watchlist.objects.update_or_create(
            user=validated_data['user'],
            movie=validated_data['movie'],
            defaults={'status': validated_data['status']}
        )
        return watchlist
