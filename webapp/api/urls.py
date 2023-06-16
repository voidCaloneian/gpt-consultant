from django.urls import path
from .views import HallViewSet, HallPriceView, BookingCreateView, CheckBookingsByDayView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hall', HallViewSet, basename='hall')

urlpatterns = [
    path('hall/price/<str:name>/', HallPriceView.as_view()),
    path('hall/bookings/<str:hall_name>/<str:date>/', CheckBookingsByDayView.as_view()),
    path('booking/', BookingCreateView.as_view())
] + router.urls
