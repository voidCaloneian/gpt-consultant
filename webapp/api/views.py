from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .models import Hall, Booking, BookingDetails
from .services import calculate_cost, calculate_delta, get_hall_by_name
from .serializers import HallDetailSerializer, HallListSerializer, HallPriceSerializer
from .utils.exceptions import InvalidDateFormat, BookingNotFound, BookingDataMissingError

import hashlib
from datetime import datetime
from dateutil.parser import parse


class HallViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Hall.objects.all()
    lookup_field = 'name'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HallDetailSerializer
        if self.action == 'list':
            return HallListSerializer
        return HallDetailSerializer
    
class HallPriceView(RetrieveAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallPriceSerializer
    lookup_field = 'name'
    
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

        if not bookings:
            raise BookingNotFound()

        bookings_dict = {
            'hall_data': {
                'opening_time': hall_opening_time.strftime('%H'),
                'closing_time': hall_closing_time.strftime('%H')
            },
            'already_booked_time_ranges_by_hours': [{
                'start': b['start_time'].strftime('%H'),
                'end': b['end_time'].strftime('%H')
            } for b in bookings]
        }
        
        return bookings_dict

class HashBookingView(APIView):
    @transaction.atomic()
    def post(self, request):
        data = request.data

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

        return Response(hash_key)


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