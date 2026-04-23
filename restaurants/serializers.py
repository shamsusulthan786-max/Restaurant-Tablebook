from rest_framework import serializers
from .models import Restaurant, Table, MenuItem, MenuCategory, Review


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description']


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'items']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'capacity']


class RestaurantSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    categories = MenuCategorySerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    tables = TableSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'address', 'city', 'description',
            'image', 'opening_time', 'closing_time',
            'average_rating', 'categories', 'reviews', 'tables'
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()