from rest_framework import serializers

from .models import Hall, Booking, BookingDetails


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDetails
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
class HallDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'
        
class HallNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('name', )

class HallTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('name', 'opening_time', 'closing_time')

class HallRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('name', 'rules')

class HallPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('name', 'price_per_hour', )

class HallDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('name', 'description')
    