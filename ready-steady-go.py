from dotenv import load_dotenv, find_dotenv
from os import environ as env
from datetime import datetime

import openai 

from halls import retro, minimalism, nature


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
openai.api_key = env.get('API_KEY')


SYSTEM_MESSAGE = f'''
    Ты - бот ассистент фотостудии, ты попунктно следуешь выполнению задач.
    Правила общения:
        1. Игнорируй сообщения, которые не относятся к работе фотостудии.
        2. Пиши только о том, что тебе было сказано.
    
    Попунктно следуй этому плану общения:
        1. Помоги клиенту выбрать зал
        2. Узнай на какую дату и на какое время клиент желает арендовать зал и на какое количество часов
        2.1 Удостоверься, что аренда зала будет проходить в диапозоне с 8:00 до 24:00, например,
            выбранное время - 15:00, а длительность аренды - 5 часов, то диапозон аренды будет -
            с 15:00 и до 20:00, но нельзя арендовать зал в 22:00, если длительность аренды более 2 часов,
            так как в 24:00 фотостудия уже закроется, и так далее.
        3. Узнай имя, номер телефона, email человека
        4. Узнай, сколько людей будет присутствовать.
        5. Расскажи о правилах выбранного зала и спроси, согласен ли клиент с ними,
        6. 
          1. Составь такую таблицу, беря соответствующую информацию из диалога (если данных для какого-то стобца нет, то узнай):
                Зал: <название_зала> (название любого зала из существующих)
                Дата: <дата_бронирования>, например: 01.01.2024, либо 25.12.2025 (Любая дата, которая не раньше текущей)
                Время: <время_бронирования> (любое время с 8:00 до 24:00, не раньше текущего времени, если дата аренды - сегодняшний день)
                Длительность: <длительность_бронирования_в_часах> (число от 1 до 16, взависимости от выбранного времени)
                Стоимость: <цена_в_час_умноженная_на_длительность> (стоимость аренды зала в час умноженная на длительность аренды)
                Имя клиента: <имя_клиента> 
                Количество людей: <количество_людей_которые_придут> (число)
                Номер телефона: <номер_телефона_клиента> (состоит из 11 цифр и только)
                Почта: <почта_клиента> (должна соответствовать формату почты)
          2. Отправь таблицу клиенту (если клиент захочет изменить какие-то данные)
            
        7. Если клиент ознакомился с данными бронирования, то отправь эту ссылку на оплату - 
           https://ссылка_на_оплату/?hall=...&date=...&time=...&duration=...&final_price=...&name=...&number_of_people=...&phone=...&email..., где
            hall=<имя_зала>
            date=<дата_бронирования>
            time=<время_бронирования>
            duration=<длительность_бронирования_в_часах>
            final_price=<цена_в_час_умноженная_на_длительность>
            name=<имя_клиента>
            number_of_people=<количество_людей_которые_придут>
            phone=<номер_телефона_клиента>
            email=<почта_клиента>
'''

def get_current_datetime():
    return datetime.now().strftime("%d.%m.%Y %H:%M")

def generate_systen_message():
    current_datetime = get_current_datetime()
    message = SYSTEM_MESSAGE + \
        f'''
            Вот описание залов: {retro}, {minimalism}, {nature}.
            Если придётся ссылаться на время, то сейчас {current_datetime}
        ''' 
    return message


def sendMessage(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        top_p=0.6,
        messages=[
            {"role": "system", "content": generate_systen_message()},
            *messages
        ]
    )
    for choice in response['choices']:
        print(choice['message']['content'])
    response_message = response['choices'][0]['message']['content']
    return response_message

def transform_chat_history(chat_history):
    transformed_chat_history_messages = list()
    for message in chat_history:
        author = message[0]
        text = message[1]
        transformed_chat_history_messages.append(
            {'role': author, 'content': text}
        )
    return transformed_chat_history_messages
    
    
chat_history = list()
while True:
    user_message = input('\n\nСообщение: ')
    chat_history.append(('user', user_message))
    response_message = sendMessage(transform_chat_history(chat_history))
    print('\n', response_message)
    chat_history.append(('assistant', response_message))

#  Добавить обработку ошибки, когда во время генерации сообщения возникает ошибка: ловить её и отправлять новый запрос на генерацию сообщения

# Step 1, send model the user query and what functions it has access to
def run_conversation():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": "What's the weather like in Boston?"}],
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]

    # Step 2, check if the model wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]

        # Step 3, call the function
        # Note: the JSON response from the model may not be valid JSON
        function_response = get_current_weather(
            location=message.get("location"),
            unit=message.get("unit"),
        )

        # Step 4, send model the info on the function call and function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": "What is the weather like in boston?"},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return second_response

print(run_conversation())
