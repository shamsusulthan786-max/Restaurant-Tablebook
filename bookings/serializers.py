from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(
        source='restaurant.name', read_only=True
    )
    table_name = serializers.CharField(
        source='table.name', read_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'restaurant', 'restaurant_name',
            'table', 'table_name', 'date', 'start_time',
            'end_time', 'party_size', 'status', 'created_at'
        ]
        read_only_fields = ['user', 'status', 'created_at']

    def validate(self, data):
        instance = Booking(**data)
        instance.clean()
        return data