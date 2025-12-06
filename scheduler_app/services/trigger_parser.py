import re
from dateparser import parse as parse_date


class TriggerParser:
    def parse(self, text: str):
        participants = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

        # naive time extraction
        date = parse_date(text)

        keywords = ["meeting", "review", "discussion", "sync", "planning"]
        title = next((k for k in keywords if k in text.lower()), "Meeting").title()

        return {
            "title": title,
            "participants": participants,
            "parsed_time": date,
            "raw": text
        }
