from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from dj_rest_auth.views import PasswordResetConfirmView
from . import views


# Custom auth-related routes
auth_patterns = [
    path("registration/", views.CustomRegisterView.as_view(), name="custom_register"),
    path('registration/verify-email/<str:uid>/<str:token>/', views.CustomVerifyEmailView.as_view(), name='custom_verify_email'),
    path('login/', TokenObtainPairView.as_view(), name='custom_login'),
    path('google/', views.GoogleLogin.as_view(), name='google_login'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', TokenBlacklistView.as_view(), name='custom_logout'),
]


urlpatterns = [
    # include custom auth patterns
    path('', include((auth_patterns))),
    # include default dj-rest-auth patterns
    path('', include('dj_rest_auth.urls')),
    # include default dj-rest-auth registration patterns
    path('registration/', include('dj_rest_auth.registration.urls')),
    
]
