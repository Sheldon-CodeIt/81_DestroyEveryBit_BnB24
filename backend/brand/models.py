from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    brand_name = models.CharField(max_length=255,default='Brand Name')  
    brand_description = models.CharField(max_length=500, default='Default description', validators=[MinLengthValidator(150)])  
 
    def __str__(self):
        return self.user.username
