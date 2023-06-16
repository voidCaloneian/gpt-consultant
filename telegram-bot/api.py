from tenacity import retry, wait_fixed, stop_after_delay
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from json import dumps
import requests


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
URL = env.get('API_URL')


class ApiHandler:
    def __init__(self):
        self.url = URL
        self.check_connection()
    
    @retry(wait=wait_fixed(30), stop=stop_after_delay(5))
    def check_connection(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            raise requests.exceptions.ConnectionError(f"Не удалось подключиться к API: {e}")
        
    def get(self, url):
        try:
            response = requests.get(self.url + url)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            return dumps({'error': str(e)})