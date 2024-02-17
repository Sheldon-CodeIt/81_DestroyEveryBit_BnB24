# In brand/admin.py

from django.contrib import admin
from .models import BrandProfile

class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number', 'is_verified', 'is_approved')  # Customize the fields displayed in the admin list view

admin.site.register(BrandProfile, BrandProfileAdmin)
