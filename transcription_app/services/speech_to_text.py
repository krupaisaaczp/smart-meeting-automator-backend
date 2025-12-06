import requests
import time
from django.conf import settings

ASSEMBLYAI_KEY = settings.ASSEMBLYAI_API_KEY

class AssemblyAIService:

    BASE = "https://api.assemblyai.com/v2"

    def upload_audio(self, local_file_path):
        """
        Uploads audio bytes directly to AssemblyAI.
        """
        headers = {"authorization": ASSEMBLYAI_KEY}
        upload_url = f"{self.BASE}/upload"

        with open(local_file_path, "rb") as f:
            while True:
                data = f.read(5_000_000)  # 5MB chunk
                if not data:
                    break
                response = requests.post(upload_url, headers=headers, data=data)
                response.raise_for_status()

        # The *last* response contains the final upload URL
        return response.json()["upload_url"]

    def request_transcription(self, upload_url):
        headers = {"authorization": ASSEMBLYAI_KEY, "content-type": "application/json"}

        json_data = {
            "audio_url": upload_url,
            "speaker_labels": True,
        }

        r = requests.post(f"{self.BASE}/transcript", json=json_data, headers=headers)
        r.raise_for_status()
        return r.json()["id"]

    def poll(self, transcript_id):
        headers = {"authorization": ASSEMBLYAI_KEY}
        url = f"{self.BASE}/transcript/{transcript_id}"

        while True:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            status = r.json()["status"]

            if status == "completed":
                return r.json()

            if status == "failed":
                raise Exception("Transcription failed")

            time.sleep(3)
