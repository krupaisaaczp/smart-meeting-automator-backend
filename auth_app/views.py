# auth_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import requests
import urllib.parse

from auth_app.models import IntegrationToken

from django.utils.crypto import get_random_string
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


import jwt
from .models import User


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from .models import User
from django.contrib.auth.hashers import make_password

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        name = data.get("name", "")

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create(
            email=email,
            full_name=name,
            password=make_password(password)
        )

        return Response({"message": "User registered successfully"})


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "refresh": str(refresh),
            "access": str(access),
        })


class MicrosoftOAuthStart(APIView):
    def get(self, request):
        auth_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
        state = get_random_string(16)

        params = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            "response_mode": "query",
            "scope": "offline_access Calendars.ReadWrite User.Read",
            "state": state,
        }

        return Response({"auth_url": auth_url + "?" + urllib.parse.urlencode(params)})
    
    
class MicrosoftOAuthCallback(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        user = request.user

        import requests

        token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

        data = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            "grant_type": "authorization_code"
        }

        res = requests.post(token_url, data=data).json()

        IntegrationToken.objects.update_or_create(
            user=user,
            service_name="microsoft_calendar",
            defaults={
                "access_token": res["access_token"],
                "refresh_token": res.get("refresh_token"),
                "expires_at": timezone.now() + timedelta(seconds=res["expires_in"])
            }
        )

        return Response({"message": "Outlook Calendar connected"})






# auth_app/views.py (add or replace)
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_app.models import IntegrationToken

class GoogleOAuthCallback(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        user = request.user
        if not code or not user or user.is_anonymous:
            return Response({"error": "Missing code or not authenticated"}, status=400)

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        resp = requests.post(token_url, data=data)
        resp.raise_for_status()
        payload = resp.json()

        # payload contains: access_token, expires_in, refresh_token (only on first consent), scope, token_type
        IntegrationToken.objects.update_or_create(
            user=user,
            service_name="google_calendar",
            defaults={
                "access_token": payload.get("access_token"),
                "refresh_token": payload.get("refresh_token"),
                "expires_at": timezone.now() + timedelta(seconds=payload.get("expires_in", 0)),
                "raw": payload,  # optional JSONField to store provider response
            }
        )

        return Response({"message": "Google connected"})
