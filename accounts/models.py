from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    preferences = models.TextField(default="{}")

    def __str__(self):
        return f"{self.user.username}'s profile"
