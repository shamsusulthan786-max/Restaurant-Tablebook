from django import forms
from django.utils import timezone
from .models import Booking

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