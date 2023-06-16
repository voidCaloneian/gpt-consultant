from rest_framework.exceptions import NotFound

from .models import Hall


def get_hall_by_name(hall_name):
    try:
        return Hall.objects.get(name=hall_name)
    except Hall.DoesNotExist:
        raise NotFound('Зал с таким именем не был найден')