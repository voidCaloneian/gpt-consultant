from tenacity import retry, wait_fixed, stop_after_attempt
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from os import environ as env
import openai 

from .conf import SystemRoleConf
from .exceptions import ChatCompletionError
from .functions import *


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
openai.api_key = env.get('OPENAIAPI_KEY')

GPT_MODEL = 'gpt-3.5-turbo-0613'

WELCOME_MESSAGE = 'Я - бот ассистент фотостудии. Я создан для помощи клиентам в выборе зала, бронировании и предоставлении информации о фотостудии. Чем могу помочь?'


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
        return {'role': 'system', 'content': self.system_message + full_current_datetime_str}
        
    def prepare_messages(self, user_message=None, temprorary_message=None):
        messages = [*self.messages,]
        
        if not temprorary_message:
            messages.append(self.generate_system_message())
        if user_message:
            messages.append({'role': 'user', 'content': user_message})
            
        return messages


class Conversation(MessageData):
    request_error_message = 'Во время обработки сообщения произошла непредвиденная ошибка'
    def __init__(self):
        super().__init__()
        self.api_handler = OpenAIHandler()

    def handle_completion(self, user_message=None):
        try:
            print('Отправляю сообщение')
            response = self.api_handler.request_completion(self.prepare_messages(user_message))
            print('Получил сообщение')
            message = response['choices'][0]['message']
            message_text = message.get('content')
            if user_message:
                self.add_message('user', user_message)

            if message.get("function_call"):
                self.handle_function_call(message)

            else:
                self.handle_assistant_message(message_text) 
        
        except ChatCompletionError as e:
            self.handle_assistant_message(e.message)

        except Exception:
            self.handle_assistant_message(self.request_error_message)
            
    def handle_function_call(self, message):
        function_name = message['function_call']['name']
        function_args = message['function_call']['arguments']

        try:
            function_response = eval(f'{function_name}(**{function_args})')
            function_message = {
                'role': 'function',
                'name': function_name,
                'content': str(function_response),
            }   
            self.messages.append(function_message)
            self.handle_completion()

        except Exception:
            self.handle_assistant_message(self.request_error_message)

    def handle_assistant_message(self, message_text):
        self.add_message('assistant', message_text) 


class OpenAIHandler:
    @retry(wait=wait_fixed(10), stop=stop_after_attempt(6), sleep=10)
    def request_completion(self, messages):
        try:
            response = openai.ChatCompletion.create(
                model=GPT_MODEL,
                temperature=0.85,
                messages=messages,
                functions=SystemRoleConf.functions,
                function_call="auto",
            )
            return response
        
        
        except (openai.error.RateLimitError, openai.error.Timeout):
            raise ChatCompletionError('Системы обработки сообщений перегружены. Попробуйте написать через 10 минут')
        
        except openai.error.AuthenticationError:
            print('С вашим API Токеном что-то не так, пересоздайте его')
            raise ChatCompletionError()
        
        except Exception as e:
            print(type(e))
            raise ChatCompletionError()