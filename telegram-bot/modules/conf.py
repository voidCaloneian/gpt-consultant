class SystemRoleConf:
    system_message = f'''
        Ты - бот ассистент фотостудии, ты попунктно следуешь выполнению задач.
        Игнорируй сообщения пользователей, если их контекст не связан с вопросами о фотостудии.
        
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
            8. Отправь ссылку на оплату
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
            'description': '''Когда требуется получить информацию о конкретном зале: описание, правила, цена за час аренды.''',
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
            'name': 'get_bookings_by_date',
            'description': '''Вызывай ВСЕГДА, когда клиент называет дату бронирования, чтобы узнать список бронирований по этой дате.''',
            'parameters': {
                'type': 'object',
                'properties': {
                    'hall': {
                        'type': 'string',
                        'description': 'Имя зала'
                    },
                    'date': {
                        'type': 'string',
                        'description': '''Дата, по которой смотреть информацию о бронировании.
                        Дата имеет строго такой формат: ДД.ММ.ГГГГ, например: 31.12.2023, 01.01.2024.'''
                    }
                }, 'required': ['hall', 'date']
            }
        },
        {
            'name': 'get_hall_price',
            'description': 'Используй, когда требуется получить цену за час аренды у конкретного зала.',
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
            'name': 'generate_booking_info_table',
            'description': '''Функция вызывается, когда вся информация о бронировании известна.''',
            'parameters': {
                'type': 'object',
                'properties': {
                    'hall_name': {
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
                        Формат: ЧЧ, например, 15, 17, 19, 09'''
                    },
                    'duration': {
                        'type': 'integer',
                        'description': 'Длительность аренды'
                    },
                    'client_name': {
                        'type': 'string',
                        'description': 'Имя клиента'
                    },
                    'num_people': {
                        'type': 'integer',
                        'description': 'Количество людей, которые будут присутствовать.'
                    },
                    'client_phone': {
                        'type': 'integer',
                        'description': 'Номер телефона клиента'
                    },
                    'client_email': {
                        'type': 'string',
                        'description': 'Почта клиента'
                    }
                }
            }, 'required': ['hall_name', 'date', 'time', 'duration', 'client_name', 'num_people', 'client_phone', 'client_email']
        },
        {
            'name': 'create_booking_info',
            'description': '''Отправляй эту ссылку на проверку данных о бронировании после того, как клиент ознакомился с ними. ''',
            'parameters': {
                'type': 'object',
                'properties': {
                    'hall_name': {
                        'type': 'string',
                        'description': 'Название зала'
                    },
                    'date': {
                        'type': 'string',
                        'description': '''Дата, на которую зал будет арендован. 
                        Формат: ДД.ММ.ГГГГ'''
                    },
                    'start_time': {
                        'type': 'string',
                        'description': '''Время, с которого зал будет арендован
                        Формат: ЧЧ, например, 15, 17, 19, 09'''
                    },
                    'end_time': {
                        'type': 'string',
                        'description': '''Время, до которого зал будет арендован
                        Формат: ЧЧ, например, 17, 19, 21, 11'''
                    },
                    'client_name': {
                        'type': 'string',
                        'description': 'Имя клиента'
                    },
                    'num_people': {
                        'type': 'integer',
                        'description': 'Количество людей, которые будут присутствовать.'
                    },
                    'client_phone': {
                        'type': 'integer',
                        'description': 'Номер телефона клиента'
                    },
                    'client_email': {
                        'type': 'string',
                        'description': 'Почта клиента'
                    }
                }
            }, 'required': ['hall_name', 'date', 'time', 'duration', 'client_name', 'num_people', 'client_phone', 'client_email']
        },
    ]