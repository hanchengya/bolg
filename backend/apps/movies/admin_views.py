from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from .models import Movie
from .serializers import MovieDetailSerializer
from apps.users.models import User
from apps.ratings.models import Rating
from apps.reviews.models import Review


class UserSerializer:
    """用户序列化器"""
    @staticmethod
    def to_dict(user):
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        }


class AdminStatsViewSet(viewsets.ViewSet):
    """管理员统计视图"""
    permission_classes = [IsAdminUser]

    def list(self, request):
        """获取统计数据"""
        print("[AdminStatsViewSet] 收到统计请求")
        try:
            user_count = User.objects.count()
            movie_count = Movie.objects.count()
            rating_count = Rating.objects.count()
            review_count = Review.objects.count()
            
            print(f"[AdminStatsViewSet] 用户数={user_count}, 电影数={movie_count}")
            
            stats = {
                'totalUsers': user_count,
                'totalMovies': movie_count,
                'totalRatings': rating_count,
                'totalReviews': review_count,
            }
            return Response(stats)
        except Exception as e:
            print(f"[AdminStatsViewSet] 错误: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)


class AdminUserViewSet(viewsets.ViewSet):
    """管理员用户管理视图"""
    permission_classes = [IsAdminUser]

    def list(self, request):
        """获取用户列表"""
        print("[AdminUserViewSet] ===== 开始处理用户列表请求 =====")
        try:
            search = request.query_params.get('search', '')
            users = User.objects.all()
            
            print(f"[AdminUserViewSet] 数据库总用户数: {users.count()}")
            
            if search:
                users = users.filter(
                    Q(username__icontains=search) | 
                    Q(email__icontains=search)
                )
                print(f"[AdminUserViewSet] 搜索 '{search}' 后: {users.count()} 个用户")
            
            users_list = list(users.order_by('-date_joined')[:100])
            print(f"[AdminUserViewSet] 查询到 {len(users_list)} 个用户")
            
            data = []
            for user in users_list:
                try:
                    user_dict = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                        'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                        'last_login': user.last_login.isoformat() if user.last_login else None,
                    }
                    data.append(user_dict)
                    print(f"[AdminUserViewSet]   - 序列化用户: {user.id} {user.username}")
                except Exception as e:
                    print(f"[AdminUserViewSet]   - 序列化用户 {user.id} 失败: {e}")
            
            print(f"[AdminUserViewSet] 成功序列化 {len(data)} 个用户")
            print(f"[AdminUserViewSet] 返回数据: {data[:2] if len(data) > 0 else '空列表'}")
            return Response(data)
        except Exception as e:
            print(f"[AdminUserViewSet] 发生错误: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

    def create(self, request):
        """创建用户"""
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            is_staff = request.data.get('is_staff', False)
            
            if User.objects.filter(username=username).exists():
                return Response(
                    {'message': '用户名已存在'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=is_staff
            )
            
            return Response(UserSerializer.to_dict(user), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, pk=None):
        """更新用户"""
        try:
            user = User.objects.get(pk=pk)
            
            if 'username' in request.data:
                user.username = request.data['username']
            if 'email' in request.data:
                user.email = request.data['email']
            if 'is_staff' in request.data:
                user.is_staff = request.data['is_staff']
            if 'password' in request.data and request.data['password']:
                user.set_password(request.data['password'])
            
            user.save()
            return Response(UserSerializer.to_dict(user))
        except User.DoesNotExist:
            return Response(
                {'message': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        """删除用户"""
        try:
            user = User.objects.get(pk=pk)
            
            # 不允许删除超级用户
            if user.is_superuser:
                return Response(
                    {'message': '不能删除超级管理员'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {'message': '用户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )


class AdminMovieViewSet(viewsets.ViewSet):
    """管理员电影管理视图"""
    permission_classes = [IsAdminUser]

    def list(self, request):
        """获取电影列表"""
        print("[AdminMovieViewSet] ===== 开始处理电影列表请求 =====")
        try:
            search = request.query_params.get('search', '')
            movies = Movie.objects.all()
            
            print(f"[AdminMovieViewSet] 数据库总电影数: {movies.count()}")
            
            if search:
                movies = movies.filter(
                    Q(title__icontains=search) | 
                    Q(director__icontains=search) |
                    Q(cast__icontains=search)
                )
                print(f"[AdminMovieViewSet] 搜索 '{search}' 后: {movies.count()} 部电影")
            
            movies_list = movies.order_by('rank')[:50]  # 限制返回前50部
            print(f"[AdminMovieViewSet] 准备返回 {len(list(movies_list))} 部电影")
            
            serializer = MovieDetailSerializer(movies_list, many=True, context={'request': request})
            data = serializer.data
            print(f"[AdminMovieViewSet] 成功序列化 {len(data)} 部电影")
            print(f"[AdminMovieViewSet] 第一个电影的poster: {data[0].get('poster') if data else 'N/A'}")
            return Response(data)
        except Exception as e:
            print(f"[AdminMovieViewSet] 发生错误: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

    def create(self, request):
        """创建电影"""
        print("[AdminMovieViewSet] 创建电影请求")
        try:
            # 打印接收到的数据
            print(f"[AdminMovieViewSet] 接收到的数据: {request.data.keys()}")
            print(f"[AdminMovieViewSet] 是否有poster文件: {'poster' in request.FILES}")
            
            # 创建电影对象
            movie_data = request.data.copy()
            
            # 如果有poster文件，Django会自动处理
            movie = Movie.objects.create(
                title=movie_data.get('title'),
                original_title=movie_data.get('original_title', ''),
                rank=movie_data.get('rank'),
                year=movie_data.get('year'),
                country=movie_data.get('country', ''),
                director=movie_data.get('director', ''),
                cast=movie_data.get('cast', ''),
                genres=movie_data.get('genres', ''),
                runtime=movie_data.get('runtime'),
                summary=movie_data.get('summary', ''),
                poster=request.FILES.get('poster'),  # 文件对象
                douban_url=movie_data.get('douban_url', ''),
                douban_rating=movie_data.get('douban_rating')
            )
            
            print(f"[AdminMovieViewSet] 电影创建成功: {movie.id} - {movie.title}")
            print(f"[AdminMovieViewSet] 海报保存为: {movie.poster}")
            
            # 返回序列化数据
            serializer = MovieDetailSerializer(movie, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"[AdminMovieViewSet] 创建电影失败: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, pk=None):
        """更新电影"""
        print(f"[AdminMovieViewSet] 更新电影 ID: {pk}")
        try:
            movie = Movie.objects.get(pk=pk)
            print(f"[AdminMovieViewSet] 找到电影: {movie.title}")
            print(f"[AdminMovieViewSet] 接收到的数据: {request.data.keys()}")
            print(f"[AdminMovieViewSet] 是否有新poster文件: {'poster' in request.FILES}")
            
            # 更新字段
            movie_data = request.data
            if 'title' in movie_data:
                movie.title = movie_data['title']
            if 'original_title' in movie_data:
                movie.original_title = movie_data['original_title']
            if 'rank' in movie_data:
                movie.rank = movie_data['rank']
            if 'year' in movie_data:
                movie.year = movie_data['year']
            if 'country' in movie_data:
                movie.country = movie_data['country']
            if 'director' in movie_data:
                movie.director = movie_data['director']
            if 'cast' in movie_data:
                movie.cast = movie_data['cast']
            if 'genres' in movie_data:
                movie.genres = movie_data['genres']
            if 'runtime' in movie_data:
                movie.runtime = movie_data['runtime']
            if 'summary' in movie_data:
                movie.summary = movie_data['summary']
            if 'douban_url' in movie_data:
                movie.douban_url = movie_data['douban_url']
            if 'douban_rating' in movie_data:
                movie.douban_rating = movie_data['douban_rating']
            
            # 如果有新上传的poster文件，更新它
            if 'poster' in request.FILES:
                movie.poster = request.FILES['poster']
                print(f"[AdminMovieViewSet] 更新海报为: {movie.poster}")
            
            movie.save()
            print(f"[AdminMovieViewSet] 电影更新成功: {movie.id}")
            
            # 返回序列化数据
            serializer = MovieDetailSerializer(movie, context={'request': request})
            return Response(serializer.data)
        except Movie.DoesNotExist:
            print(f"[AdminMovieViewSet] 电影不存在: ID={pk}")
            return Response(
                {'message': '电影不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"[AdminMovieViewSet] 更新电影失败: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        """删除电影"""
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response(
                {'message': '电影不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
