from rest_framework import serializers
from .models import Movie, Genre


class MovieListSerializer(serializers.ModelSerializer):
    """电影列表序列化器"""
    genres_list = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'rank', 'title', 'year', 'country', 'director', 'cast', 'genres',
                  'poster', 'douban_rating', 'avg_rating', 'rating_count', 'review_count', 'genres_list']

    def get_poster(self, obj):
        """返回完整的图片URL"""
        if obj.poster:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.poster.url)
            # 如果没有request，返回相对URL
            return f'/media/{obj.poster}'
        return None

    def get_genres_list(self, obj):
        """将genres字符串转换为列表"""
        if obj.genres:
            return [g.strip() for g in obj.genres.split(' / ') if g.strip()]
        return []


class MovieDetailSerializer(serializers.ModelSerializer):
    """电影详情序列化器"""
    genres_list = serializers.SerializerMethodField()
    cast_list = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'rank', 'title', 'original_title', 'year', 'country',
                  'director', 'cast_list', 'runtime', 'summary', 'poster', 'backdrop',
                  'douban_url', 'douban_rating', 'avg_rating', 'rating_count',
                  'review_count', 'genres_list', 'created_at']

    def get_poster(self, obj):
        """返回完整的图片URL"""
        if obj.poster:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.poster.url)
            # 如果没有request，返回相对URL
            return f'/media/{obj.poster}'
        return None

    def get_genres_list(self, obj):
        """将genres字符串转换为列表"""
        if obj.genres:
            return [g.strip() for g in obj.genres.split(' / ') if g.strip()]
        return []

    def get_cast_list(self, obj):
        """将cast字符串转换为列表"""
        if obj.cast:
            return [c.strip() for c in obj.cast.split(' / ') if c.strip()]
        return []


class GenreSerializer(serializers.ModelSerializer):
    """电影类型序列化器"""

    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']
