from rest_framework import generics, permissions
from .models import Restaurant, Table
from .serializers import RestaurantSerializer, TableSerializer


class RestaurantListAPIView(generics.ListAPIView):
    """
    Returns a list of all restaurants.
    Uses select_related and prefetch_related for query optimization.
    """
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Restaurant.objects.prefetch_related(
            'tables', 'reviews', 'categories', 'categories__items'
        ).all()


class RestaurantDetailAPIView(generics.RetrieveAPIView):
    """
    Returns details of a single restaurant.
    """
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Restaurant.objects.prefetch_related(
            'tables', 'reviews', 'categories', 'categories__items'
        ).all()


class TableListAPIView(generics.ListAPIView):
    """
    Returns all tables for a specific restaurant.
    """
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Table.objects.filter(
            restaurant_id=restaurant_id
        ).select_related('restaurant')