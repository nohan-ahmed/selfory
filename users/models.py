from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
# import from local
from .managers import UserManager
# Create your models here.


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Uses email as the username field.
    """
    # Basic account fields
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    # Optional personal info
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    country = CountryField(blank_label="(select country)")
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Authentication settings
    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']

    # Custom manager
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