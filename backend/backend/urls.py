from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('marketplace.urls')),  # Include marketplace URLs for the home URL
    path('brand/', include('brand.urls')), 
    path('admin/', admin.site.urls),
    # Include accounts URLs for specific URL patterns
    path('customer/', include('accounts.urls')),  # Include accounts URLs
]
