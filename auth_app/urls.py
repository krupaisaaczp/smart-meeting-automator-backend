from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MicrosoftOAuthStart,
    MicrosoftOAuthCallback
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),  # SimpleJWT refresh
    path("oauth/microsoft/start/", MicrosoftOAuthStart.as_view()),
    path("oauth/microsoft/callback/", MicrosoftOAuthCallback.as_view()),
]
