from tenacity import retry, wait_fixed, stop_after_attempt
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from json import dumps
import requests


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
URL = env.get('API_URL')


class ApiHandler:
    url = URL
    request_error_message = 'Не удалось получить ответ от сервера. Попроси клиента подождать минуту, так как сейчас на сервере неполадки'
    
    def __init__(self):
        self.check_connection()
    
    @retry(wait=wait_fixed(3), stop=stop_after_attempt(2), reraise=True)
    def check_connection(self):
        try:
            print('Проверяем соединение с API')
            response = requests.get(self.url)
            response.raise_for_status()
            print(f'Соединение с {self.url} успешно прошло проверку')
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            raise requests.exceptions.ConnectionError(f"Не удалось подключиться к API \n {e}")

    def get(self, url):
        try:
            response = requests.get(self.url + url)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            return dumps({'error': self.request_error_message})

    def post(self, url, data=None):
        try:
            response = requests.post(self.url + url, data=data)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            return dumps({'error': self.request_error_message})