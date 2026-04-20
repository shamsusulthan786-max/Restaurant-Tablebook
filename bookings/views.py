from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import datetime
from .models import Booking
from .forms import BookingForm
from restaurants.models import Restaurant, Table
from .tasks import send_booking_confirmation_email

@login_required
def booking_create(request, restaurant_id, table_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    table = get_object_or_404(Table, pk=table_id, restaurant=restaurant)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant
            booking.table = table
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Booking confirmed! A confirmation email has been sent.")
                return redirect('bookings_list')
            except ValidationError as e:
                for field, error_list in e.message_dict.items():
                    for error in error_list:
                        form.add_error(field if field in form.fields else None, error)
            except IntegrityError:
                form.add_error(None, "This table is already booked for the selected time slot.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_create.html', {
        'form': form,
        'restaurant': restaurant,
        'table': table,
    })


@login_required
def bookings_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-start_time')
    return render(request, 'bookings/bookings_list.html', {'bookings': bookings})


@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.full_clean()
                booking.save()
                messages.success(request, "Booking updated successfully.")
                return redirect('bookings_list')
            except ValidationError as e:
                for field, error_list in e.message_dict.items():
                    for error in error_list:
                        form.add_error(field if field in form.fields else None, error)
    else:
        form = BookingForm(instance=booking)

    return render(request, 'bookings/edit_booking.html', {'form': form, 'booking': booking})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.status = 'cancelled'
    booking.save()
    messages.info(request, "Booking cancelled.")
    return redirect('bookings_list')


@login_required
def available_tables(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    date = request.GET.get('date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    available_tables = Table.objects.filter(restaurant=restaurant)

    if date and start_time and end_time:
        available_tables = available_tables.exclude(
            bookings__date=date,
            bookings__start_time__lt=end_time,
            bookings__end_time__gt=start_time,
            bookings__status='confirmed'
        )

    return render(request, 'bookings/available_tables.html', {
        'restaurant': restaurant,
        'available_tables': available_tables,
    })


@login_required
def dashboard_bookings(request):
    today = datetime.today().date()
    upcoming = request.user.bookings.filter(date__gte=today, status='confirmed').order_by('date', 'start_time')
    past = request.user.bookings.filter(date__lt=today).order_by('-date')

    return render(request, 'bookings/dashboard_bookings.html', {
        'upcoming': upcoming,
        'past': past,
    })