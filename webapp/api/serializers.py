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
        
class HallListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('name', )

class HallPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('price_per_hour', )
    