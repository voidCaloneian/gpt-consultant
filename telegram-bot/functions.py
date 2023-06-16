from json import dumps

from api import ApiHandler

api_handler = ApiHandler()

def get_bookings_by_date(hall, date):
    print(get_json_response(f'hall/bookings/{hall}/{date}/'))
    return get_json_response(f'hall/bookings/{hall}/{date}/')

def get_hall_info(hall):
    return get_json_response(f'hall/{hall.capitalize()}/')

def get_hall_price(hall):
    return get_json_response(f'hall/price/{hall.capitalize()}/')

def get_halls_list():
    return get_json_response('hall/')

def get_json_response(url):
    response_json = api_handler.get(url)
    if isinstance(response_json, dict) and 'detail' in response_json:
        response_json = {'error': response_json['detail']}
    return dumps(response_json)

def generate_rental_info_table(**kwargs):
    required_params = ['duration', 'hall', 'date', 'time', 'name', 'number_of_people', 'phone', 'email']
    
    for param in required_params:
        if param not in kwargs:
            return dumps({'error': f'Отсутствует параметр: {param}'})
    
    duration = kwargs['duration']
    hall = kwargs['hall']
    
    hall_price = get_hall_price(hall).get('price_per_hour', 0)
    
    final_price = duration * hall_price
    
    table = {
        'Зал': hall,
        'Дата': kwargs['date'],
        'Время': kwargs['time'],
        'Длительность аренды': duration,
        'Стоимость': final_price,
        'Ваше имя': kwargs['name'],
        'Количество людей': kwargs['number_of_people'],
        'Номер телефона': kwargs['phone'],
        'Почта': kwargs['email']
    }
    
    return dumps(table)