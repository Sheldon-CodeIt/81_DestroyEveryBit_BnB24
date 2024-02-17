from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('', include('accounts.urls')),
    path('', include('marketplace.urls')),  # Include marketplace URLs for the home URL
    path('brand/', include('brand.urls')), 
    path('admin/', admin.site.urls),
]
