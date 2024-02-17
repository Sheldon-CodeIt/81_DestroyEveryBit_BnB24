from accounts.models import CustomerProfile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomerProfile
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
import uuid
from .models import CustomerProfile
from django.conf import settings



@login_required
def home(request):
    return render(request , 'home.html')




@csrf_exempt
def login_attempt(request):
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

    user_obj = User.objects.filter(username=username).first()
    if user_obj is None:
        return JsonResponse({'message': 'User not found.'}, status=400)

    CustomerProfile_obj = CustomerProfile.objects.filter(user=user_obj).first()

    if not CustomerProfile_obj.is_verified:
        return JsonResponse({'message': 'CustomerProfile is not verified. Check your mail.'}, status=400)

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'message': 'Wrong password.'}, status=400)

    login(request, user)
    return JsonResponse({'message': f'Hello, {username}!'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)



@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully', 'redirect': '/'})


@csrf_exempt
def password_reset(request):
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        email = data.get('email')
    else:
        email = request.POST.get('email')

    user = User.objects.filter(email=email).first()
    if user:
        auth_token = str(uuid.uuid4())
        CustomerProfile_obj, _ = CustomerProfile.objects.get_or_create(user=user)
        CustomerProfile_obj.auth_token = auth_token
        CustomerProfile_obj.save()
        send_password_reset_email(email, auth_token)
        return JsonResponse({'message': 'Password reset link sent to your email.'})
    else:
        return JsonResponse({'message': 'No user found with this email.'}, status=404)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


def send_password_reset_email(email, token):
    subject = 'Password Reset'
    message = f'Click the link to reset your password: http://127.0.0.1:8000/reset_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Deactivate older tokens
    CustomerProfile.objects.filter(user__email=email).exclude(auth_token=token).delete()

    send_mail(subject, message, email_from, recipient_list)

@csrf_exempt
def password_reset_confirm(request, auth_token):
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
    else:
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

    if new_password == confirm_password:
        CustomerProfile_obj = CustomerProfile.objects.filter(auth_token=auth_token).first()
        if CustomerProfile_obj:
            user = CustomerProfile_obj.user
            user.set_password(new_password)
            user.save()
            return JsonResponse({'message': 'Password reset successfully.'})
        else:
            return JsonResponse({'message': 'Invalid token.'}, status=400)
    else:
        return JsonResponse({'message': 'Passwords do not match.'}, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def register_attempt(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        mobile_number = data.get('mobile_number')

        try:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username is taken.'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email is taken.'}, status=400)

            user_obj = User.objects.create_user(username=username, email=email, password=password)
            auth_token = str(uuid.uuid4())
            CustomerProfile_obj = CustomerProfile.objects.create(user=user_obj, auth_token=auth_token, mobile_number=mobile_number)
            send_mail_after_registration(email, auth_token)
            return JsonResponse({'message': 'Registration successful. Check your email for verification.'}, status=201)

        except Exception as e:
            return JsonResponse({'message': 'Internal server error'}, status=500)

    return JsonResponse({'message': 'Method not allowed'}, status=405)

def success(request):
    return JsonResponse({'message': 'Success.'})

def token_send(request):
    return JsonResponse({'message': 'Token sent.'})

def verify(request, auth_token):
    try:
        CustomerProfile_obj = CustomerProfile.objects.filter(auth_token=auth_token).first()
        if CustomerProfile_obj:
            if CustomerProfile_obj.is_verified:
                return JsonResponse({'message': 'Your account is already verified.'})
            CustomerProfile_obj.is_verified = True
            CustomerProfile_obj.save()
            return JsonResponse({'message': 'Your account has been verified.'})
        else:
            return JsonResponse({'message': 'Invalid token.'}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Internal server error'}, status=500)

def error_page(request):
    return JsonResponse({'message': 'Error.'}, status=404)

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Click on this link to verify and Login http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )