from django.core.mail import send_mail
from django.conf import settings

def send_email(to, subject, body):
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [to],
        fail_silently=False,
    )
