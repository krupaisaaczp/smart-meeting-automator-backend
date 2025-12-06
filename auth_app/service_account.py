# auth_app/service_account.py
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def build_service_account_credentials(impersonate=None):
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )
    if impersonate:
        creds = creds.with_subject(impersonate)
    return creds
