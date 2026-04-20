from django.urls import path
from . import views

app_name = 'adminpanel'


urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('booking/<int:pk>/cancel/', views.admin_cancel_booking, name='admin_cancel_booking'),
    path('booking/<int:pk>/confirm/', views.admin_confirm_booking, name='admin_confirm_booking'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('create-user/', views.create_user, name='create_user'),


     # Restaurants
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/add/', views.restaurant_create, name='restaurant_create'),
    path('restaurants/<int:pk>/edit/', views.restaurant_edit, name='restaurant_edit'),
    path('restaurants/<int:pk>/delete/', views.restaurant_delete, name='restaurant_delete'),

    # Tables
    path('tables/', views.table_list, name='table_list'),
    path('tables/add/', views.table_create, name='table_create'),
    path('tables/<int:pk>/edit/', views.table_edit, name='table_edit'),
    path('tables/<int:pk>/delete/', views.table_delete, name='table_delete'),

    # Menu Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Menu Items
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),

    # Reviews
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/edit/', views.booking_edit, name='booking_edit'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),


]