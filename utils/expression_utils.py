import os
import tempfile
import requests
from playsound import playsound
from dotenv import load_dotenv

load_dotenv()

HUME_API_KEY = os.getenv("HUME_API_KEY")
HUME_VOICE = os.getenv("HUME_VOICE", "emma")

def speak(text: str, emotion: str = "neutral"):
    """
    Speaks the given text using Hume AI with emotional expression.
    """
    if not HUME_API_KEY:
        print("[HUME] Missing API key.")
        return

    try:
        print(f"[HUME] Speaking with emotion: {emotion}")
        headers = {
            "Authorization": f"Bearer {HUME_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "text": text,
            "voice": HUME_VOICE,
            "prosody": {
                "emotion": emotion
            }
        }

        response = requests.post(
            "https://api.hume.ai/v0/voice/stream",
            json=data,
            headers=headers,
            stream=True
        )

        if response.status_code == 200:
            fd, path = tempfile.mkstemp(suffix=".mp3")
            with os.fdopen(fd, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            playsound(path)
            os.remove(path)
        else:
            print(f"[HUME] Failed ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"[HUME] Error occurred: {e}")