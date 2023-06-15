from tenacity import retry, wait_fixed, stop_after_attempt
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from os import environ as env
import openai 

from conf import SystemRoleConf
from functions import get_hall_info, get_hall_price, get_halls_list, generate_rental_info_table


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
        
    def prepare_messages(self, user_message, ghost_function_message=None):
        messages = [
            {'role': 'assistant', 'content': self.system_message + f'Текущая дата: {datetime.now().strftime("%d.%m.%Y %H:%M")}'}, *self.messages,
        ]
        if user_message:
            messages.append({'role': 'user', 'content': user_message})
        if ghost_function_message:
            messages.append(ghost_function_message)
        return messages


class Conversation(MessageData):
    def __init__(self):
        super().__init__()
        self.api_handler = OpenAIHandler()

    def handle_completion(self, user_message=None, ghost_function_message=None):
        response = self.api_handler.request_completion(self.prepare_messages(user_message, ghost_function_message))
        message = response['choices'][0]['message']
        message_text = message.get('content')
        
        if user_message:
            self.add_message('user', user_message)

        if message.get("function_call"):
            self.handle_function_call(message, response)
            
        else:
            self.handle_assistant_message(message_text) 
            
    def handle_function_call(self, message, response):
        function_name = message['function_call']['name']
        function_args = message['function_call']['arguments']
        function_response = eval(f'{function_name}(**{function_args})')

        full_message = response['choices'][0]
        ghost_function_message = {
            "role": "function",
            "name": full_message["message"]["function_call"]["name"],
            "content": str(function_response),
        }   
            
        self.handle_completion(ghost_function_message=ghost_function_message)
    
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
print('Здравствуйте, кто вы')
conv.handle_completion('Здравствуйте, кто вы')
print(conv.messages[-1]['content'])
print('Я хотел бы арендовать зал')
conv.handle_completion('Я хотел бы арендовать зал')
print(conv.messages[-1]['content'])
print('Меня интересует зал минимализм')
conv.handle_completion('Меня интересует зал минимализм')
print(conv.messages[-1]['content'])
print('Хотя давайте лучше зал ретро')
conv.handle_completion('Хотя давайте лучше зал ретро')
print(conv.messages[-1]['content'])
