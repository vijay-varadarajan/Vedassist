from django.contrib import admin

# Register your models here.
from .models import *


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'medicine_price')  # Adjust the fields as per your model
    
admin.site.register(Medicine, MedicineAdmin)