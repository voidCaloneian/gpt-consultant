# Примечание!
## Из-за ажиотажа вокруг новой модели бота могут возникать трудности во время работы с ним: обработка запросов генерации сообщений может занимать либо слишком большое время (минуты), либо вовсе вызывать ошибки из-за перегруженности самой модели. Также из-за этого не было возможности протестировать бота в полной мере.
# Вне зависимости от системного сообщения, бот может перестать ему следовать, если стиль/манера/слова в вашем сообщении хоть на грамм поменяются
## Установка проекта:
```
git clone https://github.com/voidCaloneian/gpt-consultant.git
cd gpt-consultant
python webapp\manage.py makemigrations
python webapp\manage.py migrate
python webapp\manage.py initdata
echo Установка проекта прошла успешно!
```
### Примечание!
### Команда ```python webapp\manage.py initdata``` (!!!БЫЛА УЖЕ ВЫПОЛНЕНА ВО ВРЕМЯ УСТАНОВКИ ПРОЕКТА!!!) инициализирует данные для тестирования проекта, а именно:
  - Создаёт 3 заранее подготовленных зала
  - Создаёт в случайном количестве бронирования на следующие 10 дней (настройки генерации можно поменять в **webapp\api\management\commands\initdata.py**
  - Создаёт аккаунт администратора для админ панели сайта. Логин - theresa | Пароль - qwe123
## В корневой папке проекта (где находится .gitignore, README.md) в файле **.env** выполните эти действия:
- Укажите свой OpenAI API Key **OPENAIAPI_KEY** 
- Укажите токен своего телеграмм бота **TELEGRAMBOT_TOKEN** 
## Запуск проекта:
### Запуск сервера:
  ```python webapp\manage.py runserver```
### Запуск телеграмм-бота:
  ```python telegram-bot\main.py```
  
# Структура проекта:
- **webapp** - содержит сервер на Django для обработки запросов бота.
- **telegram-bot** - содержит файлы, необходимые для работы телеграм-бота:
  - **main.py** - отвечает за работу телеграмм-бота, написанного на асинхронном фреймворке aiogram, который позволяет боту отправлять несколько chat completion запросов, не дожидаясь ответов на сообщения друг друга.
  - **modules/api.py** - отвечает за взаимодействие бота с API сервера.
  - **modules/conf.py** - содержит инструкции для бота построения диалога, также содержит описание того, как ему взаимодействовать с функциями
  - **modules/conversation.py** - отвечает за взаимодействие с **OpenAI API**
  - **modules/exceptions.py** - содержит логику ошибок, которые могут возникнуть
  - **modules/functions.py** - содержит логику кастомных функции, которые бот может вызывать
    
## Описание работы бота
Бот работает на модели **gpt-3.5-turbo-0613**, ключевой особенностью которой является возможность вызова кастомных функций.
Функции, которые бот использует во время общения с клиентом:
- **get_halls_data** - позволяет получить конкретную информацию сразу обо всех залах, будь то: описание, время открытия и закрытия, правила, цена
- **get_hall_info** - получает информацию о конкретном зале по его имени, в нашем случае: название зала, его описание, правила и цена в час, время открытия и закрытия.
- **get_hall_price** - получает цену за час аренды конкретного зала. Нужна функция для того, чтобы бот быстрее обрабатывал запрос, получая только нужную себе цену, а не всю информацию о зале через функцию **get_hall_info**
- **get_bookings_by_date** - получает список бронирований по конкретной дате у конкретного зала.
- **generate_booking_info** - генерирует таблицу с данными о бронировании. Вызывается перед созданием объекта бронирования для того, чтобы клиент мог свериться с данными в таблице и изменить что-то, если это нужно.
- **create_booking_info** - создаёт объект бронирования (в базе данных сервера) для последующей генерации ссылки на оплату (ключ ссылки на оплату - сгенерированный hash ключ, основанный на информации о бронировании).
## Страница информации о бронировании
![image](https://github.com/voidCaloneian/gpt-consultant/assets/106653303/8f9f289a-2763-4f86-ac86-c0825241517f)

## Для конечного результата в проект требовалось бы добавить:
- Celery Для удаления бронирований, которые не были оплачены в течении 3 дней
- ElasticSearch Для fuzzy-поиска залов по имени (для того, чтобы клиент, знающий, какие залы есть, даже если бы ошибся в имени, мог бы получить информацию о зале)
- Возможность клиенту самому корректировать данные на странице проверки информации о бронировании перед оплатой 

### Ознакомиться с вызовом функций с использованием модели **gpt-3.5-turbo-0613** можно здесь:
- https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
- https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_for_knowledge_retrieval.ipynb

