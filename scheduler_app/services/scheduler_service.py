from datetime import timedelta
from django.utils import timezone
import random

class SchedulerService:
    def find_available_slot(self, preferred_time=None, duration=30):
        # Mock slot finder
        base = preferred_time or timezone.now() + timedelta(hours=2)
        slot = base.replace(minute=0, second=0, microsecond=0)
        
        # mock delay variation
        slot += timedelta(hours=random.choice([0, 1, 2]))

        return slot

    def generate_meeting_link(self):
        return f"https://meet.fakeplatform.com/{random.randint(100000,999999)}"
