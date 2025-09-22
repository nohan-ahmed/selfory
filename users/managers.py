from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email) # Normalize the email
        user = self.model(email=email, username=username, **extra_fields) # Create the user
        user.set_password(password) # Hash the password
        # Save the user to the database using the specified database
        user.save(using=self._db) 
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        # Create a superuser with the given email, username, and password
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)
# Note: Ensure that the User model in users/models.py uses this UserManager