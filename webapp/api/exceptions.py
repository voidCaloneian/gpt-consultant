from rest_framework.exceptions import APIException


class InvalidDateFormat(APIException):
    status_code = 400
    default_detail = 'Invalid date format. Date should be in format "DD.MM.YYYY".'

class HallNotFound(APIException):
    status_code = 404
    default_detail = 'Hall not found.'

class BookingNotFound(APIException):
    status_code = 404
    default_detail = 'Bookings not found for the specified date.'