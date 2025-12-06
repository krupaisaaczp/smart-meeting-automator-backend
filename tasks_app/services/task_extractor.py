import spacy
from dateparser import parse as dp
import re
from .models import Task
from auth_app.models import User
nlp = spacy.load("en_core_web_sm")

def create_tasks_from_actions(meeting, actions, confidence_default=0.75):
    created = []
    for a in actions:
        owner_obj = None
        owner_email = a.get("owner_email")
        owner_name = a.get("owner")
        if owner_email:
            owner_obj = User.objects.filter(email__iexact=owner_email).first()
        else:
            # try to match owner name to user full_name
            if owner_name:
                owner_obj = User.objects.filter(full_name__icontains=owner_name).first()

        deadline = None
        if a.get("deadline"):
            try:
                deadline = dp(a["deadline"])
            except Exception:
                deadline = None

        # Use heuristics to derive priority
        pr = "medium"
        lowtext = a["text"].lower()
        if any(k in lowtext for k in ("urgent","asap","immediately")):
            pr = "high"

        task = Task.objects.create(
            meeting=meeting,
            description=a["text"],
            owner=owner_obj,
            owner_email=owner_email if not owner_obj else None,
            deadline=deadline,
            priority=pr,
            confidence_score=confidence_default
        )
        created.append(task)
    return created
