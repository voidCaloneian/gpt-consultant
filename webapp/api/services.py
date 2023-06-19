from django.db.utils import IntegrityError

from .utils.exceptions import HallNotFound
from .models import Hall

from datetime import datetime, time, timedelta


def get_hall_by_name(hall_name):
    try:
        return Hall.objects.get(name=hall_name)
    except Hall.DoesNotExist:
        raise HallNotFound()
    
def calculate_cost(hall, delta=None, hours=None):
        try:
            price_per_hour = hall.price_per_hour
            if delta:
                cost = price_per_hour * delta.total_seconds() // 3600
            elif hours:
                cost = price_per_hour * int(hours)
            else:
                raise ValueError('Необходимо указать хотя бы один из параметров: либо "delta", либо "hours"')
            
            if cost <= 0:
                raise ValueError('Начало бронирования должно быть РАНЬШЕ, чем конец бронирования')
            
            return cost
        except AttributeError:
            raise AttributeError("Не удалось вычислить стоимость.")

from datetime import datetime, time, timedelta

def calculate_delta(start_time, end_time):
    try:
        today = datetime.today()
        start_datetime = datetime.combine(today, start_time)
        end_datetime = datetime.combine(today, end_time)
        
        # Round start and end datetimes to the nearest hour
        if start_datetime.minute > 0:
            start_rounded = start_datetime.replace(minute=0) + timedelta(minutes=60)
        if end_datetime.minute > 0:
            end_rounded = end_datetime.replace(minute=0) + timedelta(minutes=60)
        print(end_rounded, start_rounded)
        return end_rounded - start_rounded
    except TypeError:
        raise TypeError("Неверный формат времени. Время должно быть в формате 'ЧЧ:ММ:СС'.")


        