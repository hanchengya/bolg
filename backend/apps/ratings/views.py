from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from .models import Rating
from .serializers import RatingSerializer, RatingListSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """评分视图集"""
    permission_classes = [IsAuthenticated]
    pagination_class = None  # 关闭分页，直接返回所有评分

    def get_serializer_class(self):
        """根据不同的操作返回不同的序列化器"""
        if self.action in ['list', 'retrieve']:
            return RatingListSerializer
        return RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user).select_related('movie')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.save()

        # 更新电影的平均评分
        movie = rating.movie
        avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg('score'))['score__avg']
        rating_count = Rating.objects.filter(movie=movie).count()
        movie.avg_rating = round(avg_rating, 1) if avg_rating else 0
        movie.rating_count = rating_count
        movie.save()

        # 返回包含电影详情的数据
        return_serializer = RatingListSerializer(rating)
        return Response(return_serializer.data, status=status.HTTP_201_CREATED)
