import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.management import call_command
from django.contrib.auth.models import User

from api.models import Hall, Booking


class Command(BaseCommand):
    halls_data = (
    {
        "name": "Минимализм",
        "description": "Студия с современным минималистичным дизайном. Идеально подходит для продуктовой фотографии или редакционных съемок.",
        "rules": "На белые полы нельзя ходить в обуви, нельзя трогать световое оборудование. Не оставляйте мусор и грязь после использования.",
        "price_per_hour": 3750,
        "opening_time": "10:00",
        "closing_time": "23:00"
    },
    {
        "name": "Мрак",
        "description": "Зал с темной отделкой и эффектами освещения, создающими атмосферу таинственности и интриги. Подходит для съемок фильмов ужасов, мистических клипов, а также для проведения тематических вечеринок.",
        "rules": "Нельзя использовать источники открытого огня, курить в помещении, разбрасывать мусор или повреждать оборудование. Необходимо бережно относиться к реквизиту.",
        "price_per_hour": 5000,
        "opening_time": "11:00",
        "closing_time": "19:00"
    },
    {
        "name": "Пустота",
        "description": "Просторный зал с голыми стенами и минималистичным интерьером, создающим эффект пространства и свободы. Подходит для танцевальных вечеринок, спортивных тренировок, фотосессий с акцентом на модели или одежду.",
        "rules": "Необходимо следить за порядком и чистотой, не повреждать оборудование и не использовать запрещенные категорией вещества. Нельзя курить в помещении.",
        "price_per_hour": 4450,
        "opening_time": "17:00",
        "closing_time": "21:00"
    }
)

    def handle(self, *args, **options):
        self.create_halls()
        self.create_random_bookings()
        self.create_super_user()
            
    def create_halls(self):
        for hall_data in self.halls_data:
            Hall.objects.create(**hall_data)
        
        print('Залы были успешно созданы')
    
    def create_random_bookings(self, days=10, payload_percentage=50, max_booking_length=3):
        '''
        days - максимальное различие в дате от текущей даты при создании бронирования
        payload_percentage - процент нагруженности, где 10+ - очень мало бронирований, 50+ - среднее количество, 100+ - очень большая нагруженность
        max_booking_length - максимальная длительность бронирования в часах
        '''
        today = timezone.now().date()
        start_of_week = today

        for hall in Hall.objects.all():
            opening_time = hall.opening_time
            closing_time = hall.closing_time
            
            for _ in range(int(0.6 * payload_percentage)):
                day_datetime = start_of_week + timedelta(days=random.randint(1, days))
                start_hour = random.randint(opening_time.hour, closing_time.hour - max_booking_length)
                start_minute = 0
                start_time = timezone.datetime.combine(day_datetime, timezone.datetime.min.time()) + timedelta(hours=start_hour, minutes=start_minute)

                end_time = start_time + timedelta(hours=random.randint(1, max_booking_length))
                
                overlapping_bookings = Booking.objects.filter(hall=hall, date=start_time.date(), start_time__lt=end_time, end_time__gt=start_time)
                
                if not overlapping_bookings.exists():
                    Booking.objects.create(hall=hall, date=start_time.date(), start_time=start_time.time(), end_time=end_time.time())
                    
        print('Бронирования на следующие', days, 'были успешно созданы')
        
    def create_super_user(self):
        username = 'theresa'
        email = 'theresa@example.com'
        password = 'qwe123'
        call_command("createsuperuser", '--username', username, '--email', email, interactive=False)
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        
        print('Данные для входа в админ панель: имя - theresa | пароль - qwe123')