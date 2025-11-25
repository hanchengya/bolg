from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet

router = DefaultRouter()
router.register(r'', RatingViewSet, basename='rating')

app_name = 'ratings'

urlpatterns = router.urls
