from datetime import datetime, timedelta
from googleapiclient.discovery import build
from django.utils import timezone
from auth_app.models import IntegrationToken

class CalendarService:
    def __init__(self, user):
        self.user = user

    def _google_service(self):
        token = IntegrationToken.objects.get(user=self.user, service_name="google_calendar")

        from google.oauth2.credentials import Credentials
        creds = Credentials(
            token.access_token,
            refresh_token=token.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET
        )

        return build("calendar", "v3", credentials=creds)

    def find_available_slots(self, participants, duration):
        """ Query free/busy API """
        service = self._google_service()

        time_min = timezone.now().isoformat()
        time_max = (timezone.now() + timedelta(days=1)).isoformat()

        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": p.email} for p in participants]
        }

        result = service.freebusy().query(body=body).execute()

        # Simplified: assume earliest mutual free slot 1 hour from now
        return timezone.now() + timedelta(hours=1)

    def create_event(self, meeting):
        service = self._google_service()

        event_body = {
            "summary": meeting.title,
            "description": meeting.description,
            "start": {"dateTime": meeting.scheduled_time.isoformat()},
            "end": {
                "dateTime": (meeting.scheduled_time + timedelta(minutes=meeting.duration_minutes)).isoformat()
            },
            "attendees": [{"email": u.email} for u in meeting.participants.all()]
        }

        event = service.events().insert(calendarId="primary", body=event_body).execute()

        meeting.meeting_link = event.get("hangoutLink")
        meeting.calendar_event_id = event.get("id")
        meeting.save()

        return meeting


# calendar_service.py (new file, maybe in scheduler_app/services)
import uuid
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_calendar_event(credentials, meeting):
    """
    credentials: google.oauth2.credentials.Credentials or service-account Credentials
    meeting: your Meeting model instance (with title, description, scheduled_time, duration_minutes, participants (emails list))
    Returns event dict.
    """
    service = build("calendar", "v3", credentials=credentials, cache_discovery=False)

    start = meeting.scheduled_time.isoformat()
    end = (meeting.scheduled_time + timedelta(minutes=meeting.duration_minutes)).isoformat()

    attendees = []
    for u in meeting.participants.all():
        attendees.append({"email": u.email})

    event_body = {
        "summary": meeting.title,
        "description": meeting.description or "",
        "start": {"dateTime": start, "timeZone": "UTC"},
        "end": {"dateTime": end, "timeZone": "UTC"},
        "attendees": attendees,
        # request Google Meet conference
        "conferenceData": {
            "createRequest": {
                "requestId": str(uuid.uuid4())
            }
        },
        "reminders": {"useDefault": True},
    }

    try:
        event = service.events().insert(
            calendarId="primary",
            body=event_body,
            conferenceDataVersion=1,  # required to create Meet link
            sendUpdates="all"  # or "none" — sends invitations
        ).execute()
    except HttpError as e:
        raise

    # hangoutLink or conferenceData.entryPoints[*] may contain the URL
    meet_link = event.get("hangoutLink")
    if not meet_link and event.get("conferenceData"):
        entry_points = event["conferenceData"].get("entryPoints", [])
        for ep in entry_points:
            if ep.get("entryPointType") in ("video", "more"):
                meet_link = ep.get("uri")
                break

    return {"event": event, "meet_link": meet_link}
