import requests
from django.conf import settings

def send_slack_message(text):
    webhook_url = settings.SLACK_WEBHOOK_URL
    payload = {"text": text}
    requests.post(webhook_url, json=payload)
