import os
from django.conf import settings
from uuid import uuid4

def save_local_file(file_obj, filename=None):
    filename = filename or f"{uuid4()}.wav"

    audio_dir = os.path.join(settings.MEDIA_ROOT, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    path = os.path.join(audio_dir, filename)

    with open(path, "wb") as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    return path  # local path only
