from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(user_email, restaurant_name, date, start_time, end_time):
    send_mail(
        'Booking Confirmation',
        f'Your booking at {restaurant_name} for {date} {start_time}-{end_time} is confirmed.',
        'noreply@restaurantapp.com',
        [user_email],
        fail_silently=True,
    )