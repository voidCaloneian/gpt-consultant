from json import dumps

from .api import ApiHandler


api_handler = ApiHandler()


def get_bookings_by_date(hall, date):
    response = get_json_response(f'hall/bookings/{hall}/{date}/')
    return response

def get_hall_info(hall):
    return get_json_response(f'hall/{hall.capitalize()}/')

def get_hall_price(hall):
    return get_json_response(f'hall/price/{hall.capitalize()}/', dumping=False)

def get_halls_data(data_type):
    return get_json_response(f'hall/?data={data_type}')

def generate_booking_info(hall_name, date, time, duration, client_name, num_people, client_phone, client_email):
    hall_price = get_hall_price(hall_name).get('price_per_hour', 0)
    
    final_price = duration * hall_price
    
    table = {
        'Зал': hall_name,
        'Дата': date,
        'Время': time,
        'Длительность аренды': duration,
        'Стоимость': final_price,
        'Ваше имя': client_name,
        'Количество людей': num_people,
        'Номер телефона': client_phone,
        'Почта': client_email
    }
    
    return dumps(table)

def create_booking_info(hall_name, date, start_time, end_time, client_name, client_email, client_phone, num_people):
    data = {
        hall_name: hall_name,
        client_name: client_name,
        client_email: client_email,
        client_phone: client_phone,
        date: date,
        start_time: start_time,
        end_time: end_time,
        num_people: num_people
    }
    return get_json_response('booking/', dumping=False, post=True, data=data)

def get_json_response(url, dumping=True, post=False, data=None):
    if post:
        response_json = api_handler.post(url, data=data)
    else:
        response_json = api_handler.get(url)
        
    if isinstance(response_json, dict) and 'detail' in response_json:
        response_json = {'error': response_json['detail']}
        
    return dumps(response_json) if dumping else response_json