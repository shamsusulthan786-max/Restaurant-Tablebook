from django.urls import path
from .views import (
    bookings_list,booking_create, cancel_booking, edit_booking, available_tables, dashboard_bookings,
)
from .api_views import BookingListAPIView, BookingCreateAPIView, BookingCancelAPIView

urlpatterns = [
    # List all bookings for the logged-in user
    path('', bookings_list, name='bookings_list'),

    # Create a booking for a specific restaurant + table
    path('create/<int:restaurant_id>/<int:table_id>/', booking_create, name='booking_create'),

    # Cancel a booking
    path('cancel/<int:pk>/', cancel_booking, name='cancel_booking'),

    # Edit/modify a booking
    path('edit/<int:pk>/', edit_booking, name='edit_booking'),

    # Show available tables for a restaurant (real-time availability)
    path('available/<int:restaurant_id>/', available_tables, name='available_tables'),

    # Dashboard view: upcoming + past bookings
    path('dashboard/', dashboard_bookings, name='dashboard_bookings'),


    # API endpoints
    path('api/', BookingListAPIView.as_view(), name='api_booking_list'),
    path('api/create/', BookingCreateAPIView.as_view(), name='api_booking_create'),
    path('api/cancel/<int:pk>/', BookingCancelAPIView.as_view(), name='api_booking_cancel'),
]