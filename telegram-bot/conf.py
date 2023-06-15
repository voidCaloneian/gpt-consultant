class SystemRoleConf:
    system_message = f'''
        Ты - бот ассистент фотостудии, ты попунктно следуешь выполнению задач.
        Правила общения:
            1. Игнорируй сообщения, которые не относятся к работе фотостудии.
        
        Попунктно следуй этому плану общения:
            1. Помоги клиенту выбрать зал
            2. Узнай на какую дату и на какое время клиент желает арендовать зал и на какое количество часов
            2.1 Удостоверься, что зал можно будет арендовать на это время
            3. Узнай имя, номер телефона, email человека
            4. Узнай, сколько людей будет присутствовать.
            5. Расскажи о правилах выбранного зала и спроси, согласен ли клиент с ними,
            6. Убедись, что узнал у клиента ВСЕ нужные данные: 
                Название зала, дату и время аренды, длительность аренды, имя клиента, количество людей, которые придут, 
                номер телефона клиента, почту клиента.
            7. Составь таблицу информации аренды зала
    '''
    functions = [
            {
                'name': 'get_halls_list',
                'description': 'Когда требуется получить список названий залов',
                'parameters': {
                    'type': 'object',
                    'properties': {},
                }
            },
            {
                'name': 'get_hall_info',
                'description': '''Когда требуется получить информацию о конкретном зале. 
                Ты НИКОГДА не должен использовать эту функцию до того, пока в этом диалога не была вызвана функция get_halls_list.''',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'hall': {
                            'type': 'string',
                            'description': 'Имя зала'
                        }
                    }
                }, 'required': ['hall',]
                
            },
            {
                'name': 'get_hall_price',
                'description': 'Используй ВСЕГДА, когда требуется получить цену за час аренды у конкретного зала',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'hall': {
                            'type': 'string',
                            'description': 'Имя зала'
                        }
                    }
                }, 'required': ['hall',]
            },
            {
                'name': 'generate_rental_info_tabel',
                'description': '''Кога нужно составить таблицу информации аренды зала. ''',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'hall': {
                            'type': 'string',
                            'description': 'Название зала'
                        },
                        'date': {
                            'type': 'string',
                            'description': '''Дата, на которую зал будет арендован. 
                            Формат: ДД.ММ.ГГГГ'''
                        },
                        'time': {
                            'type': 'string',
                            'description': '''Время, на которое зал будет арендован
                            Формат: ЧЧ:ММ'''
                        },
                        'duration': {
                            'type': 'integer',
                            'description': 'Длительность аренды'
                        },
                        'name': {
                            'type': 'string',
                            'description': 'Имя клиента'
                        },
                        'number_of_people': {
                            'type': 'integer',
                            'description': 'Количество людей, которые будут присутствовать.'
                        },
                        'phone': {
                            'type': 'integer',
                            'description': 'Номер телефона клиента'
                        },
                        'email': {
                            'type': 'string',
                            'description': 'Почта клиента'
                        }
                    }
                }, 'required': ['hall', 'date', 'time', 'duration', 'name', 'number_of_people', 'phone', 'email']
            }
        ]