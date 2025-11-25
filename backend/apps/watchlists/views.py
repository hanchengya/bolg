from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Watchlist
from .serializers import WatchlistSerializer, WatchlistCreateSerializer


class WatchlistViewSet(viewsets.ModelViewSet):
    """观影清单视图集"""
    permission_classes = [IsAuthenticated]
    pagination_class = None  # 关闭分页

    def get_queryset(self):
        queryset = Watchlist.objects.filter(user=self.request.user).select_related('movie')

        # 按状态筛选
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return WatchlistCreateSerializer
        return WatchlistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        watchlist = serializer.save()

        # 返回完整的watchlist信息
        return_serializer = WatchlistSerializer(watchlist)
        return Response(return_serializer.data, status=status.HTTP_201_CREATED)
