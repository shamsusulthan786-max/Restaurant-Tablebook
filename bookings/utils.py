from datetime import datetime, time
from .models import Booking

def is_table_available(table, date, start_time, end_time):
    overlaps = Booking.objects.filter(
        table=table, date=date,
        start_time__lt=end_time,
        end_time__gt=start_time,
        status='confirmed'
    ).exists()
    return not overlaps