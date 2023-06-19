from django.urls import path

from .views import (
    HallViewSet, 
    HallPriceView, 
    CheckBookingsByDayView, 
    HashBookingView,
    CheckoutView
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('hall', HallViewSet, basename='hall')

urlpatterns = [
    path('hall/price/<str:name>/', HallPriceView.as_view()),
    path('hall/bookings/<str:hall_name>/<str:date>/', CheckBookingsByDayView.as_view()),
    path('booking/', HashBookingView.as_view()),
    path('booking/checkout/<str:hash_key>/', CheckoutView.as_view())
] + router.urls
