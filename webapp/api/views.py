from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Hall, Booking
from .services import get_hall_by_name
from .serializers import HallDetailSerializer, HallListSerializer, HallPriceSerializer

from datetime import datetime, timedelta


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
        date_obj = datetime.strptime(date, '%d.%m.%Y').date()

        hall = get_hall_by_name(hall_name)
        hall_opening_time = hall.opening_time
        hall_closing_time = hall.closing_time

        bookings = Booking.objects.filter(hall=hall, date=date_obj).values('date', 'start_time', 'end_time')

        bookings_dict = {
            'hall_data': {
                'opening_time': hall_opening_time.strftime('%H'),
                'closing_time': hall_closing_time.strftime('%H')
            },
            'bookings_by_hours': [{
                'start': b['start_time'].strftime('%H'),
                'end': b['end_time'].strftime('%H')
            } for b in bookings]
        }
        
        if len(bookings_dict['bookings_by_hours']) == 0:
            bookings_dict['bookings_by_hours'] = 'Бронирований на эту дату нет. Зал в этот день свободен'

        return Response(bookings_dict)
    

class AvailableDatesView(APIView):
    def get(self, request, hall_name, days=31):
        hall = get_hall_by_name(hall_name)
        hall_opening_time = hall.opening_time
        hall_closing_time = hall.closing_time
        
        available_dates = []
        today = datetime.today().date()
        end_date = today + timedelta(days=days)

        bookings = Booking.objects.filter(hall=hall)
        for date in self.daterange(today, end_date):
            if self.date_is_available(date, bookings, hall_opening_time, hall_closing_time):
                available_dates.append(date.strftime('%d.%m.%Y'))

        return Response(available_dates)

    @staticmethod
    def daterange(start_date, end_date):
        """Вспомогательная функция, возвращает генератор дат между двумя датами."""
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)
    
    @staticmethod
    def date_is_available(date, bookings, hall_opening_time, hall_closing_time):
        bookings_by_date = bookings.filter(date=date)
        if bookings.exists() and \
            bookings_by_date.filter(start_time=hall_opening_time).exists() and \
                bookings_by_date.filter(end_time=hall_closing_time).exists():
                return False
        return True