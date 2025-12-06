# auth_app/google_utils.py
import time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from django.conf import settings
from auth_app.models import IntegrationToken

def get_google_credentials_for_user(user):
    token = IntegrationToken.objects.filter(user=user, service_name="google_calendar").first()
    if not token:
        return None

    creds = Credentials(
        token=token.access_token,
        refresh_token=token.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    if not creds.valid and creds.expired and creds.refresh_token:
        request = Request()
        creds.refresh(request)
        # update DB with new tokens
        token.access_token = creds.token
        token.expires_at = timezone.now() + timedelta(seconds=(creds.expiry - timezone.now()).total_seconds()) if creds.expiry else None
        token.save()
    return creds
