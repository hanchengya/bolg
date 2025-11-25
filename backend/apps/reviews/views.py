from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Review, Comment
from .serializers import (
    ReviewListSerializer,
    ReviewDetailSerializer,
    ReviewCreateSerializer,
    CommentSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    """影评视图集"""
    queryset = Review.objects.select_related('user', 'movie').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # 关闭分页

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReviewDetailSerializer
        elif self.action == 'create' or self.action == 'update':
            return ReviewCreateSerializer
        return ReviewListSerializer

    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'movie').all()

        # 按电影筛选
        movie_id = self.request.query_params.get('movie')
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)

        # 按用户筛选
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def helpful(self, request, pk=None):
        """标记影评有用"""
        review = self.get_object()
        review.helpful_count += 1
        review.save()
        return Response({'message': '已标记为有用'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """获取影评的评论列表"""
        review = self.get_object()
        comments = review.comments.select_related('user').all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        """添加评论"""
        review = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review=review)
            review.comment_count += 1
            review.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
