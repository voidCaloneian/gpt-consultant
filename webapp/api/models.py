from django.db import models
from django.core.exceptions import ValidationError

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
        if self.start_time < self.hall.opening_time:
            raise ValidationError('Время начала бронирования должно быть после времени открытия зала.')
        if self.end_time > self.hall.closing_time:
            raise ValidationError('Время окончания бронирования должно быть до времени закрытия зала.')
        if self.start_time >= self.end_time:
            raise ValidationError('Время начала бронирования должно быть до времени окончания бронирования.')
        
