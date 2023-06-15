from django.urls import path
from .views import HallViewSet, HallPriceAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hall', HallViewSet, basename='hall')

urlpatterns = [
    path('hall/price/<str:name>/', HallPriceAPIView.as_view())
] + router.urls
