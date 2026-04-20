from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from restaurants.models import Restaurant, Table

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookings')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    party_size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    class Meta:
        ordering = ['date', 'start_time']
        constraints = [
            models.UniqueConstraint(fields=['table', 'date', 'start_time', 'end_time'], name='unique_booking_slot')
        ]

    def clean(self):
        errors = {}
        now = timezone.localtime()

        # ✅ Prevent booking in the past (date+time check)
        if self.date and self.start_time:
            start_dt = datetime.combine(self.date, self.start_time)
            start_dt = timezone.make_aware(start_dt, timezone.get_current_timezone())
            if start_dt < now:
                errors['start_time'] = "You cannot book a time slot that has already passed."

        # ✅ End time must be after start time
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                errors['end_time'] = "End time must be after start time."

        # ✅ Party size check
        if self.party_size and self.table_id:
            table = Table.objects.filter(pk=self.table_id).first()
            if table and self.party_size > table.capacity:
                errors['party_size'] = "Party size exceeds table capacity."

        # ✅ Prevent overlapping bookings
        if self.table_id and self.date and self.start_time and self.end_time:
            overlapping = Booking.objects.filter(
                table_id=self.table_id,
                date=self.date,
                status='confirmed'
            ).exclude(pk=self.pk).filter(
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
            if overlapping.exists():
                errors['start_time'] = "This table is already booked for the selected time slot."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.restaurant.name} {self.table.name} {self.date} {self.start_time}-{self.end_time}'