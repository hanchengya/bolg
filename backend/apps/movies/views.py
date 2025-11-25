from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Movie, Genre
from .serializers import MovieListSerializer, MovieDetailSerializer, GenreSerializer
from .ai_config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_OPTIONS, OLLAMA_TIMEOUT
import requests
import json
import os


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """电影视图集"""
    queryset = Movie.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'original_title', 'director', 'cast']
    ordering_fields = ['rank', 'douban_rating', 'avg_rating', 'year', 'created_at']
    ordering = ['rank']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieListSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()

        # 按年份筛选
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)

        # 按类型筛选
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genres__contains=genre)

        # 按评分筛选
        rating_gte = self.request.query_params.get('rating_gte')
        if rating_gte:
            queryset = queryset.filter(douban_rating__gte=rating_gte)

        return queryset

    @action(detail=False, methods=['get'], pagination_class=None)
    def top_rated(self, request):
        """获取高分电影"""
        limit = int(request.query_params.get('limit', 10))
        movies = Movie.objects.filter(douban_rating__gte=9.0).order_by('-douban_rating')[:limit]
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], pagination_class=None)
    def years(self, request):
        """获取所有电影的年份列表"""
        years = Movie.objects.filter(year__isnull=False).values_list('year', flat=True).distinct().order_by('-year')
        return Response(list(years))

    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索电影"""
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(original_title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )[:20]

        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """电影类型视图集"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def movie_chat(request):
    """电影AI聊天接口"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return Response({
                'success': False,
                'error': '消息不能为空'
            }, status=400)
        
        # 调用Ollama API - 使用当前选择的模型
        ollama_response = requests.post(
            f'{OLLAMA_BASE_URL}/api/generate',
            json={
                'model': CURRENT_MODEL,
                'prompt': user_message,
                'stream': False,
                'options': OLLAMA_OPTIONS
            },
            timeout=OLLAMA_TIMEOUT
        )
        
        if ollama_response.status_code == 200:
            result = ollama_response.json()
            return Response({
                'success': True,
                'response': result['response']
            })
        else:
            return Response({
                'success': False,
                'error': f'Ollama API错误: {ollama_response.status_code}'
            }, status=500)
            
    except requests.exceptions.Timeout:
        return Response({
            'success': False,
            'error': '请求超时，请稍后重试'
        }, status=504)
    except requests.exceptions.ConnectionError:
        return Response({
            'success': False,
            'error': 'AI服务暂时不可用'
        }, status=503)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def movie_recommend(request):
    """电影推荐接口"""
    try:
        data = json.loads(request.body)
        genre = data.get('genre', '')
        
        prompt = f"推荐一部{genre}电影" if genre else "推荐一部好看的电影"
        
        ollama_response = requests.post(
            f'{OLLAMA_BASE_URL}/api/generate',
            json={
                'model': OLLAMA_MODEL,
                'prompt': prompt,
                'stream': False
            },
            timeout=30
        )
        
        if ollama_response.status_code == 200:
            result = ollama_response.json()
            return Response({
                'success': True,
                'recommendation': result['response']
            })
        else:
            return Response({
                'success': False,
                'error': 'API调用失败'
            }, status=500)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


# 全局变量来存储当前使用的模型
CURRENT_MODEL = OLLAMA_MODEL


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_models(request):
    """获取可用的AI模型列表"""
    try:
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            # 过滤出电影相关的模型
            movie_models = [
                {
                    'name': model['name'],
                    'size': f"{model['size'] / (1024**3):.2f} GB",
                    'modified_at': model['modified_at'],
                    'is_current': model['name'] == CURRENT_MODEL or model['name'].startswith(CURRENT_MODEL)
                }
                for model in models
                if 'movie' in model['name'].lower()
            ]
            
            return Response({
                'success': True,
                'models': movie_models,
                'current_model': CURRENT_MODEL
            })
        else:
            return Response({
                'success': False,
                'error': f'获取模型列表失败: {response.status_code}'
            }, status=500)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def switch_model(request):
    """切换AI模型（仅管理员）"""
    global CURRENT_MODEL
    
    # 验证用户是否为管理员
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response({
            'success': False,
            'error': '需要管理员权限'
        }, status=401)
    
    try:
        from rest_framework_simplejwt.tokens import AccessToken
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        
        from apps.users.models import User
        user = User.objects.get(id=user_id)
        
        if not user.is_staff and not user.is_superuser:
            return Response({
                'success': False,
                'error': '需要管理员权限'
            }, status=403)
    except Exception as e:
        return Response({
            'success': False,
            'error': '认证失败'
        }, status=401)
    
    try:
        data = json.loads(request.body)
        model_name = data.get('model_name', '')
        
        if not model_name:
            return Response({
                'success': False,
                'error': '模型名称不能为空'
            }, status=400)
        
        # 验证模型是否存在
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=10)
        if response.status_code == 200:
            models = response.json().get('models', [])
            available_models = [m['name'] for m in models]
            
            if model_name not in available_models:
                return Response({
                    'success': False,
                    'error': f'模型 {model_name} 不存在'
                }, status=404)
            
            # 切换模型
            CURRENT_MODEL = model_name
            
            # 更新配置文件
            config_path = os.path.join(os.path.dirname(__file__), 'ai_config.py')
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 替换模型配置
                import re
                new_content = re.sub(
                    r'OLLAMA_MODEL = ["\'].*?["\']',
                    f'OLLAMA_MODEL = "{model_name}"',
                    content
                )
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
            except Exception as e:
                print(f"Warning: Failed to update config file: {e}")
            
            return Response({
                'success': True,
                'message': f'已切换到模型: {model_name}',
                'current_model': CURRENT_MODEL
            })
        else:
            return Response({
                'success': False,
                'error': '无法验证模型'
            }, status=500)
            
    except json.JSONDecodeError:
        return Response({
            'success': False,
            'error': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_model(request):
    """获取当前使用的模型"""
    return Response({
        'success': True,
        'current_model': CURRENT_MODEL
    })
