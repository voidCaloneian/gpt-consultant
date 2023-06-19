from rest_framework.exceptions import APIException


class BookingDataMissingError(APIException):
    status_code = 400
    default_detail = 'Отсутствуют обязательные поля'
    
    def __init__(self, missing_fields):
        self.missing_fields = missing_fields
        super().__init__()

    def to_dict(self):
        return {'error': self.default_detail, 'missing_fields': self.missing_fields}

class InvalidDateFormat(APIException):
    status_code = 400
    default_detail = 'Неправильный формат даты. Дата должна быть в формате: ДД.ММ.ГГГГ'

class HallNotFound(APIException):
    status_code = 404
    default_detail = 'Зал не был найден'

class BookingNotFound(APIException):
    status_code = 404
    default_detail = 'Не найдено бронирований на эту дату. Зал в этот день полностью свободен'