from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, UserCredit

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the User model.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    # List view settings
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)

    # Field groups for change view
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'date_of_birth',
                'profile_pic',  # fixed: was 'profile_picture'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Field groups for add view
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )


@admin.register(UserCredit)
class UserCreditAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "credits", "updated_at", "created_at")
    search_fields = ("user__username", "user__email")
