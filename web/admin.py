from django.contrib import admin

# Register your models here.
from .models import Customers, Employees, Geodata, Orders, Products

admin.site.register(Customers)
admin.site.register(Employees)
admin.site.register(Geodata)
admin.site.register(Orders)
admin.site.register(Products)