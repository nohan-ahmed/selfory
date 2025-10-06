from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
# rest framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# allauth import
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_account_settings
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
# import local
from .serializers import CustomRegisterSerializer
from .models import User
# Create your views here.

"""
CustomRegisterView
------------------
Why:
By default, dj-rest-auth + allauth only send a verification email if the new user
is created as active (user.is_active = True). If we immediately deactivate the user
inside the serializer, no email is sent. This causes the "no confirmation email"
problem when forcing email verification.

How it works:
This custom view overrides `perform_create` to:
1. Call the default serializer.save() to create the user.
2. Run `complete_signup`, which triggers allauth's email confirmation flow.
3. After the email is sent, set user.is_active = False to ensure the account is
   locked until the email is verified.

Result:
- Verification email is always sent.
- User cannot log in until they confirm their email address.
"""

class CustomRegisterView(BaseRegisterView):
    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.setdefault("is_active", False) # set is_active to False
        user = serializer.save()
        
        # Generate uid and token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Send verification email
        # verification_link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}" # for production
        verification_link = f"{request.build_absolute_uri('/api/users/registration/verify-email/')}{uid}/{token}/" # for development
        subject = "Verify your email"
        
        # Render the HTML template with context
        message = render_to_string('./users/verification_mail.html',{
                'user': user,
                'verification_link': verification_link,
            })
        
        send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])
        
        return Response({"message": "Signed up successfully. Check your email to verify your account"}, status=status.HTTP_201_CREATED)


class CustomVerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)
        
            
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)



