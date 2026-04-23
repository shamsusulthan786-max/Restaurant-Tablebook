from django.urls import path
from . import views
from .api_views import RestaurantListAPIView, RestaurantDetailAPIView, TableListAPIView

app_name = 'restaurants'

urlpatterns = [
    # Regular views
    path('', views.restaurant_list, name='restaurant_list'),
    path('<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('<int:restaurant_id>/review/', views.add_review, name='add_review'),

    # API endpoints
    path('api/', RestaurantListAPIView.as_view(), name='api_restaurant_list'),
    path('api/<int:pk>/', RestaurantDetailAPIView.as_view(), name='api_restaurant_detail'),
    path('api/<int:restaurant_id>/tables/', TableListAPIView.as_view(), name='api_table_list'),
]