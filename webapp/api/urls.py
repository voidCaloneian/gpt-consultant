from django.urls import path

from .views import (
    HallDetailView, 
    HallPriceView, 
    CheckBookingsByDayView, 
    HashBookingView,
    CheckoutView,
    HallDataView
)


urlpatterns = [
    path('hall/<str:name>/', HallDetailView.as_view()),
    path('hall/', HallDataView.as_view(), name='get-halls-data'),
    path('hall/price/<str:name>/', HallPriceView.as_view(), name='get-hall-price'),
    path('hall/bookings/<str:hall_name>/<str:date>/', CheckBookingsByDayView.as_view(), name='check-by-day'),
    
    path('booking/', HashBookingView.as_view(), name='checkout-generate'),
    path('booking/checkout/<str:hash_key>/', CheckoutView.as_view(), name='checkout')
] 
