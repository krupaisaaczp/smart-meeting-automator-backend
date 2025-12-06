class AgendaGenerator:
    def generate(self, meeting):
        participants = [p.full_name or p.email for p in meeting.participants.all()]
        participant_list = "- " + "\n- ".join(participants)

        agenda = f"""
Agenda for {meeting.title}

Participants:
{participant_list}

Objectives:
- Clarify meeting goals
- Align on project requirements
- Identify risks
- Define next steps

Discussion Points:
1. Overview of current progress
2. Key blockers and challenges
3. Proposed solutions
4. Action items and owners

Expected Outcomes:
- Decisions documented
- Tasks assigned
- Follow-up meeting scheduled (if needed)
"""
        return agenda.strip()
