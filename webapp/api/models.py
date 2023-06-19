from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from datetime import datetime, timedelta


SHA_256_LENGTH = 64


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
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    hash_key = models.CharField(max_length=SHA_256_LENGTH, null=True, blank=True) 
    is_paid = models.BooleanField(default=False, null=True, blank=True)
    details = models.ForeignKey('BookingDetails', on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save()
        self.full_clean()
    
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
        
        do_we_save = False
        
        if start_datetime.minute > 0:
            start_rounded = start_datetime.replace(minute=0) + timedelta(minutes=60)
            self.start_time = start_rounded.time()
            do_we_save = True
            
        if end_datetime.minute > 0:
            end_rounded = end_datetime.replace(minute=0) + timedelta(minutes=60)
            self.end_time = end_rounded.time()
            do_we_save = True
            
        if do_we_save:
            self.save()
        
    def _validate_existing_bookings(self):
        existing_bookings = Booking.objects.filter(
            models.Q(date=self.date),
            models.Q(hall=self.hall),
            models.Q(start_time__lt=self.end_time) & models.Q(end_time__gt=self.start_time)
        ).exclude(id=self.id)
        
        if existing_bookings.exists():
            raise ValidationError('На это время зал уже забронирован.')
    
    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y")} {self.hall}: с {self.start_time} до {self.end_time}'

class BookingDetails(models.Model):
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_email = models.EmailField(null=True, blank=True)
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    num_people = models.IntegerField(null=True, blank=True)
    cost = models.PositiveIntegerField(blank=True)