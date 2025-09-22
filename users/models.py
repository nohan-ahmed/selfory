from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# import from local
from .managers import UserManager

# Create your models here.

class User(AbstractUser):
    # Add custom fields here, if needed
    username = models.CharField(max_length=150, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)

    # Set the username field as the email field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()

    def __str__(self):
        return self.username

class UserCredit(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_credits')
    credits = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.credits} credits"