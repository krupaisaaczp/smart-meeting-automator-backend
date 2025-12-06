from transcription_app.models import Summary
from notifications_app.services.email_service import send_email

def send_meeting_summary(meeting):
    try:
        summary = meeting.summary
    except:
        return

    attendees = meeting.attendees.all()

    subject = f"Meeting Summary: {meeting.title}"
    body = (
        f"Key Points:\n{summary.key_points}\n\n"
        f"Decisions:\n{summary.decisions}\n\n"
        f"Action Items:\n{summary.deadlines}\n\n"
        f"Full Summary:\n{summary.full_summary}"
    )

    for user in attendees:
        send_email(user.email, subject, body)
        send_slack_message(f"Summary for meeting '{meeting.title}' is ready.")

