from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Restaurant(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return self.name
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(r.rating for r in reviews) / reviews.count()
        return 0

    def clean(self):
        if self.opening_time and self.closing_time:
            # Allow midnight (00:00) as a valid closing time
            from datetime import time
            if self.closing_time != time(0, 0) and self.closing_time <= self.opening_time:
                raise ValidationError("Closing time must be after opening time.")


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    name = models.CharField(max_length=50)  # e.g., T1, Window-2
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.restaurant.name} - {self.name} ({self.capacity})'


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.restaurant.name} - {self.name}'


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # 1–5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} → {self.restaurant.name} ({self.rating})'

    def clean(self):

        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")