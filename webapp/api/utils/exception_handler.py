from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(exc, context)
    print(type(exc))
   
    if response is not None:
        response.data['status_code'] = response.status_code
        return response
    if isinstance(exc, APIException):
        error_dict = {'error': exc.detail}

        if hasattr(exc, 'missing_fields'):
            error_dict['missing_fields'] = exc.missing_fields

        return Response(error_dict, status=exc.status_code)

    return Response({'error': str(exc)}, status=400)
