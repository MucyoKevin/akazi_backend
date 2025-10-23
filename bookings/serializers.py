from rest_framework import serializers
from .models import Booking, BookingAvailability

class BookingSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.user.username', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    platform_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'service', 'provider', 'scheduled_date', 'scheduled_time',
            'service_address', 'additional_notes', 'status', 'total_amount',
            'platform_fee', 'provider_name', 'service_name', 'created_at'
        ]
        read_only_fields = ['id', 'customer', 'status', 'platform_fee', 'created_at']

class BookingAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingAvailability
        fields = ['date', 'time_slots', 'is_available']
