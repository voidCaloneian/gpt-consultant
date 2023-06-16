from tenacity import retry, wait_fixed, stop_after_attempt
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from os import environ as env
import openai 

from conf import SystemRoleConf
from functions import get_hall_info, get_bookings_by_date, get_hall_price, get_halls_list, generate_rental_info_table


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
openai.api_key = env.get('OPENAIAPI_KEY')

GPT_MODEL = 'gpt-3.5-turbo-0613'


class MessageData(SystemRoleConf):
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})
    
    def generate_system_message(self):
        weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        
        current_datetime = datetime.now()
        current_datetime_str = current_datetime.strftime("%d.%m.%Y %H:%M")
        current_weekday_str = weekdays[current_datetime.weekday()]
        
        full_current_datetime_str = f'Текущая дата и время: {current_datetime_str}, текущий день недели: {current_weekday_str}.'
        return {'role': 'assistant', 'content': self.system_message + full_current_datetime_str}
        
    def prepare_messages(self, user_message, temprorary_message=None):
        messages = [
            self.generate_system_message(), *self.messages,
        ]
        if user_message:
            messages.append({'role': 'user', 'content': user_message})
        if temprorary_message:
            messages.append(temprorary_message)
        return messages


class Conversation(MessageData):
    def __init__(self):
        super().__init__()
        self.api_handler = OpenAIHandler()

    def handle_completion(self, user_message=None, temprorary_message=None):
        response = self.api_handler.request_completion(self.prepare_messages(user_message, temprorary_message))
        message = response['choices'][0]['message']
        message_text = message.get('content')
        
        if user_message:
            self.add_message('user', user_message)

        if message.get("function_call"):
            self.handle_function_call(message)
            
        else:
            self.handle_assistant_message(message_text) 
            
    def handle_function_call(self, message):
        function_name = message['function_call']['name']
        function_args = message['function_call']['arguments']
        
        function_response = eval(f'{function_name}(**{function_args})')

        function_message = {
            'role': 'function',
            'name': function_name,
            'content': str(function_response),
        }   
            
        self.handle_completion(temprorary_message=function_message)
    
    def handle_assistant_message(self, message_text):
        self.add_message('assistant', message_text) 


class OpenAIHandler:
    @retry(wait=wait_fixed(30), stop=stop_after_attempt(3))
    def request_completion(self, messages):
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            temperature=0,
            messages=messages,
            functions = SystemRoleConf().functions,
            function_call="auto",
        )
        return response

conv = Conversation()

while True:
    conv.handle_completion(input('Ваше сообщение: '))
    print(conv.messages[-1].get('content'))