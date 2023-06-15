from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound

from datetime import datetime, timedelta


class Hall(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_hour = models.PositiveBigIntegerField()
    rules = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def clean(self):
        if self.opening_time >= self.closing_time:
            raise ValidationError('Время открытия должно быть раньше, чем время закрытия.')
        
    def __str__(self):
        return self.name

class Booking(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def clean(self):
        self._validate_booking_time()
        self._validate_booking_duration()
        self._validate_existing_bookings()

    def _validate_booking_time(self):
        if self.start_time < self.hall.opening_time:
            raise ValidationError('Время начала бронирования должно быть после времени открытия зала.')
        if self.end_time > self.hall.closing_time:
            raise ValidationError('Время окончания бронирования должно быть до времени закрытия зала.')
        if self.start_time >= self.end_time:
            raise ValidationError('Время начала бронирования должно быть до времени окончания бронирования.')

    def _validate_booking_duration(self):
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = datetime.combine(self.date, self.end_time)

        # Округляем время окончания бронирования до ближайшего часа
        end_hour = (end_datetime.minute // 60) + end_datetime.hour
        end_datetime = end_datetime.replace(hour=end_hour, minute=0)

        duration = end_datetime - start_datetime

        # Проверяем, что длительность бронирования - целое число часов
        if duration.total_seconds() % 3600 != 0:
            raise ValidationError('Длительность бронирования должна быть кратна часу')

    def _validate_existing_bookings(self):
        existing_bookings = Booking.objects.filter(
            models.Q(date=self.date),
            models.Q(hall=self.hall),
            models.Q(start_time__lt=self.end_time) & models.Q(end_time__gt=self.start_time)
        ).exclude(id=self.id)
        
        if existing_bookings.exists():
            raise ValidationError('На это время зал уже забронирован.')
    
    def available_dates(self, hall_name: str, days=31):
        try:
            hall = Hall.objects.get(name=hall_name)
        except Hall.DoesNotExist:
            raise NotFound('Зал с таким именем не был найден')
        hall_opening_time = hall.opening_time
        hall_closing_time = hall.closing_time
        
        available = []
        today = datetime.today().date()
        end_date = today + timedelta(days=days)

        bookings = Booking.objects.filter(hall=hall)
        for date in self.daterange(today, end_date):
            bookings_by_date = bookings.filter(date=date)
            if bookings_by_date.filter(start_time=hall_opening_time).exists() and \
                bookings_by_date.filter(end_time=hall_closing_time).exists():
                    continue
            else:
                available.append(date.strftime('%d.%m.%Y'))

        return available

    @staticmethod
    def daterange(start_date, end_date):
        """
        Вспомогательная функция, возвращает генератор дат между двумя датами.
        """
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)
    
    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y")} {self.hall}: с {self.start_time} до {self.end_time}'
