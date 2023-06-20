from django.urls import path, include

from .views import *


def ping(*args):
    return HttpResponse('pong')
    
hall_urls = [
    path('', HallDataView.as_view(), name='get-halls-data'),
    path('<str:name>/', HallDetailView.as_view()),
    path('price/<str:name>/', HallPriceView.as_view(), name='get-hall-price'),
    path('bookings/<str:hall_name>/<str:date>/', CheckBookingsByDayView.as_view(), name='check-by-day')
]

booking_urls = [
    path('', HashBookingView.as_view(), name='checkout-generate'),
    path('checkout/<str:hash_key>/', CheckoutView.as_view(), name='checkout')
]

urlpatterns = [
    path('', ping), 
    path('hall/', include(hall_urls)),
    path('booking/', include(booking_urls)),
] 
