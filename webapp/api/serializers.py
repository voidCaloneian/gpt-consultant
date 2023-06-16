from rest_framework import serializers

from .models import Hall, Booking, BookingDetails

from datetime import datetime


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDetails
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    date = serializers.CharField(write_only=True)
    hall_name = serializers.CharField(write_only=True, required=False)
    details = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        try:
            date = validated_data.pop('date')
            details_data = validated_data.pop('details', None)
            hall_name = validated_data.pop('hall_name')
            hall = Hall.objects.get(name=hall_name)

            start_time = validated_data.get('start_time')
            end_time = validated_data.get('end_time')

            date = self.parse_date(date)
            delta = self.calculate_delta(start_time, end_time)

            booking = self.create_booking(validated_data, hall, date)

            if details_data:
                cost = self.calculate_cost(hall, delta)
                details = self.create_details(details_data, cost)
                booking.details = details

            booking.clean()
            booking.save()

            return booking

        except Exception as e:
            raise serializers.ValidationError(str(e))

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Неверный формат даты. Дата должна быть в формате 'ДД.ММ.ГГГГ'.")

    def calculate_delta(self, start_time, end_time):
        try:
            today = datetime.today()
            start_datetime = datetime.combine(today, start_time)
            end_datetime = datetime.combine(today, end_time)
            return end_datetime - start_datetime
        except TypeError:
            raise TypeError("Неверный формат времени. Время должно быть в формате 'ЧЧ:ММ:СС'.")

    def create_booking(self, validated_data, hall, date):
        try:
            booking = Booking(
                date=date,
                hall=hall,
                **validated_data
            )
            booking.full_clean()
            booking.save()
            return booking
        except Exception as e:
            raise ValueError(str(e))

    def calculate_cost(self, hall, delta):
        try:
            price_per_hour = hall.price_per_hour
            cost = price_per_hour * delta.total_seconds() // 3600
            return cost
        except AttributeError:
            raise AttributeError("Не удалось вычислить стоимость.")

    def create_details(self, details_data, cost):
        try:
            details = BookingDetails.objects.create(
                cost=cost,
                **details_data
            )
            return details
        except Exception as e:
            raise ValueError(str(e))
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.details:
            ret['details'] = BookingDetailsSerializer(instance.details).data
        return ret
        
class HallDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'
        
class HallListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('name', )

class HallPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('price_per_hour', )
    