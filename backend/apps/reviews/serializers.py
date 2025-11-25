from rest_framework import serializers
from .models import Review, Comment
from apps.users.serializers import UserSerializer
from apps.movies.serializers import MovieListSerializer


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'parent', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ReviewListSerializer(serializers.ModelSerializer):
    """影评列表序列化器"""
    user = UserSerializer(read_only=True)
    movie = MovieListSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'title', 'content', 'contains_spoilers',
                  'helpful_count', 'comment_count', 'created_at']


class ReviewDetailSerializer(serializers.ModelSerializer):
    """影评详情序列化器"""
    user = UserSerializer(read_only=True)
    movie = MovieListSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'title', 'content', 'contains_spoilers',
                  'helpful_count', 'comment_count', 'created_at', 'updated_at', 'comments']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """影评创建序列化器"""

    class Meta:
        model = Review
        fields = ['movie', 'title', 'content', 'contains_spoilers']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
