from rest_framework.exceptions import APIException


class InvalidDateFormat(APIException):
    status_code = 400
    default_detail = 'Неправильный формат даты. Дата должна быть в формате: ДД.ММ.ГГГГ'

class HallNotFound(APIException):
    status_code = 404
    default_detail = 'Зал не был найден'

class BookingNotFound(APIException):
    status_code = 404
    default_detail = 'Не найдено бронирований на эту дату.'