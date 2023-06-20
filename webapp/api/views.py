from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction
from django.urls import reverse
from django.views import View

from .serializers import *
from .models import Hall, Booking, BookingDetails
from .services import calculate_cost, calculate_delta, get_hall_by_name
from .utils.exceptions import InvalidDateFormat, BookingDataMissingError, BookingNotFound

import hashlib
from datetime import datetime
from dateutil.parser import parse


URL = 'http://127.0.0.1:8000'


class HallDetailView(RetrieveAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallDetailSerializer
    lookup_field = 'name'
    
class HallPriceView(RetrieveAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallPriceSerializer
    lookup_field = 'name'
    
class HallDataView(ListAPIView):
    queryset = Hall.objects.all()
    
    def get_serializer_class(self):
        data = self.request.GET.get('data')
        if data == 'price':
            return HallPriceSerializer
        elif data == 'description':
            return HallDescriptionSerializer
        elif data == 'rule':
            return HallRulesSerializer
        elif data == 'time':
            return HallTimeSerializer
        elif data == 'name':
            return HallNameSerializer
        else:
            raise ValueError('''
                Тип данных', data, 'ты не можешь получить, вот список доступных типов данных:
                price, description, rule, time, name'''
            )
    
class CheckBookingsByDayView(APIView):
    def get(self, request, hall_name, date):
        hall = get_hall_by_name(hall_name)
        
        hall_opening_time = hall.opening_time
        hall_closing_time = hall.closing_time

        try:
            date_obj = datetime.strptime(date, '%d.%m.%Y').date()
        except ValueError:
            raise InvalidDateFormat()

        bookings = Booking.objects.filter(hall=hall, date=date_obj).values('date', 'start_time', 'end_time')
        if bookings.count() == 0:
            raise BookingNotFound()

        bookings_dict = {
            'hall_data': {
                'opening_time': hall_opening_time.strftime('%H'),
                'closing_time': hall_closing_time.strftime('%H')
            },
            'already_booked_time_ranges_by_hours': [{
                'start': b['start_time'].replace(hour=b['start_time'].hour - 1, minute=59).strftime('%H'),
                'end': b['end_time'].replace(hour=b['start_time'].hour - 1, minute=59).strftime('%H')
            } for b in bookings]
        }
        print(bookings_dict)
        return Response(bookings_dict)

class HashBookingView(APIView):
    @transaction.atomic()
    def post(self, request):
        data = request.data
        print('123')
        required_fields = ['hall_name', 'date', 'start_time', 'end_time', 'client_name', 'client_email', 'client_phone', 'num_people']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise BookingDataMissingError(missing_fields)
        
        hall_name = data['hall_name']
        client_name = data['client_name']
        client_email = data['client_email']
        client_phone = data['client_phone']
        num_people = data['num_people']
        
        date = parse(data['date']).date()
        start_time = parse(data['start_time']).time()
        end_time = parse(data['end_time']).time()
        

        hall = get_hall_by_name(hall_name)
        cost = calculate_cost(
            hall,
            calculate_delta(start_time, end_time)
        )

        details = BookingDetails.objects.create(
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            num_people=num_people,
            cost=cost
        )

        booking = Booking(
            hall=hall,
            date=date,
            start_time=start_time,
            end_time=end_time,
            details=details,
            is_paid=False,
        )

        hash_object = hashlib.sha256(str(booking).encode('utf-8'))
        hash_key = hash_object.hexdigest()

        booking.hash_key = hash_key
        
        booking.save()

        return Response(
            {'link': URL + reverse('checkout', args=[hash_key])}
        )


class CheckoutView(View):
    template_name = 'checkout.html'

    def get(self, request, hash_key):
        try:
            booking = Booking.objects.get(hash_key=hash_key)
        except Booking.DoesNotExist:
            return HttpResponse('Хэш ключ не валиден.')
        
        if booking.details is not None:
            details = booking.details
    
        context = {
            'booking': booking,
            'details': details,
            'date': booking.date.strftime('%d.%m.%Y'),
            'start_time': booking.start_time.strftime('%H:%M'),
            'end_time': booking.end_time.strftime('%H:%M'),
        }
        return render(request, self.template_name, context)