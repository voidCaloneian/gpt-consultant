from django.urls import path

from .views import (
    HallViewSet, 
    HallPriceView, 
    CheckBookingsByDayView, 
    HashBookingView,
    CheckoutView,
    HallDataView
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('hall', HallViewSet, basename='hall')

urlpatterns = [
    path('hall/', HallDataView.as_view(), name='get-halls-data'),
    path('hall/price/<str:name>/', HallPriceView.as_view(), name='get-hall-price'),
    path('hall/bookings/<str:hall_name>/<str:date>/', CheckBookingsByDayView.as_view(), name='check-by-day'),
    
    path('booking/', HashBookingView.as_view(), name='checkout-generate'),
    path('booking/checkout/<str:hash_key>/', CheckoutView.as_view(), name='checkout')
] + router.urls
