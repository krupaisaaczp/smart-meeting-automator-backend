import uuid
from datetime import timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth_app.google_utils import get_google_credentials_for_user
from auth_app.service_account import build_service_account_credentials


def build_event_body(meeting):
    start = meeting.scheduled_time.isoformat()
    end = (meeting.scheduled_time + timedelta(minutes=meeting.duration_minutes)).isoformat()

    attendees = [{"email": u.email} for u in meeting.participants.all()]

    return {
        "summary": meeting.title,
        "description": meeting.description or "",
        "start": {"dateTime": start, "timeZone": "UTC"},
        "end": {"dateTime": end, "timeZone": "UTC"},
        "attendees": attendees,
        "conferenceData": {
            "createRequest": {
                "requestId": str(uuid.uuid4())
            }
        },
        "reminders": {"useDefault": True},
    }


def sync_meeting_to_google(meeting):
    """
    Try user OAuth first.
    If user hasn't connected Google: fall back to service account.
    """
    try:
        creds = get_google_credentials_for_user(meeting.organizer)
        if not creds:
            creds = build_service_account_credentials()
        service = build("calendar", "v3", credentials=creds, cache_discovery=False)

        event_body = build_event_body(meeting)

        event = service.events().insert(
            calendarId="primary",
            body=event_body,
            conferenceDataVersion=1,
            sendUpdates="all"
        ).execute()

        meet_link = None
        if event.get("hangoutLink"):
            meet_link = event["hangoutLink"]

        if not meet_link and event.get("conferenceData"):
            for ep in event["conferenceData"].get("entryPoints", []):
                if ep.get("entryPointType") in ("video", "more"):
                    meet_link = ep.get("uri")
                    break

        if meet_link:
            meeting.meeting_link = meet_link
            meeting.save()

        return event

    except Exception as exc:
        print("Google Calendar sync failed:", exc)
        return None
