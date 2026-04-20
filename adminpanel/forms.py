from django import forms
from django.contrib.auth.models import User
from restaurants.models import Restaurant, Table, MenuCategory, MenuItem, Review
from bookings.models import Booking
from django.utils import timezone



class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_active']


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'city', 'description', 'image', 'opening_time', 'closing_time']

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['restaurant', 'name', 'capacity']

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['restaurant', 'name']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'price', 'description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['restaurant', 'user', 'rating', 'comment']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time', 'party_size']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    # ✅ restrict to today and future dates
                    'min': timezone.localdate().isoformat()
                }
            ),
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    # ✅ initial min set to current time
                    'min': timezone.localtime().strftime("%H:%M")
                }
            ),
            'end_time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'party_size': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1}
            ),
        }


