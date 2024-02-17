from django.urls import path
from .views import *
from django.http import JsonResponse

def hello(request):
    return JsonResponse({'message': 'Hello!'})

urlpatterns = [
    path('', hello, name="home"),
    path('customer/register/', register_attempt, name="register_attempt"),
    path('customer/login/', login_attempt, name="login_attempt"),
    path('customer/token/', token_send, name="token_send"),
    path('customer/success/', success, name='success'),
    path('customer/verify/<auth_token>/', verify, name="verify"),
    path('customer/error/', error_page, name="error"),
    path('customer/logout/', logout_view, name='logout'),
    path('customer/reset_password/', password_reset, name='password_reset'),
    path('customer/reset_password/<str:auth_token>/', password_reset_confirm, name='password_reset_confirm'),
]
