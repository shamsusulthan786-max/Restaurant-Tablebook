from django.contrib import admin
from .models import Restaurant, Table, MenuCategory, MenuItem, Review


# Register your models here.
admin.site.register([Restaurant, Table, MenuCategory, MenuItem, Review])