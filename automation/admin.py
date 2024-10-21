from django.contrib import admin
from .models import *

@admin.register(Student)
class AdminStudent(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll_number', 'age', 'std_class']
    list_filter = ['name']
    list_per_page = 30 
