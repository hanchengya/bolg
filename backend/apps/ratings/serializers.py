from rest_framework import serializers
from .models import Rating
from apps.movies.serializers import MovieListSerializer


class RatingSerializer(serializers.ModelSerializer):
    """评分序列化器（用于创建/更新）"""
    score = serializers.FloatField()  # 确保score返回为浮点数

    class Meta:
        model = Rating
        fields = ['id', 'movie', 'score', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # 使用update_or_create来处理评分的更新
        rating, created = Rating.objects.update_or_create(
            user=validated_data['user'],
            movie=validated_data['movie'],
            defaults={'score': validated_data['score']}
        )
        return rating


class RatingListSerializer(serializers.ModelSerializer):
    """评分列表序列化器（包含电影详情）"""
    movie_detail = MovieListSerializer(source='movie', read_only=True)
    score = serializers.FloatField()  # 确保score返回为浮点数

    class Meta:
        model = Rating
        fields = ['id', 'movie', 'movie_detail', 'score', 'created_at', 'updated_at']
        read_only_fields = ['id', 'movie_detail', 'created_at', 'updated_at']
