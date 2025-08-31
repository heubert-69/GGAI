import os
import tempfile
import requests
from playsound import playsound
from dotenv import load_dotenv

# Load API key
load_dotenv()
HUME_API_KEY = os.getenv("HUME_API_KEY")

LETTER_PATH = "letters/my_roman_empire.txt"

def play_easter_egg(emotion="love"):
    """
    Reads a love letter from file and uses Hume's expressive TTS to play it.
    """
    if not HUME_API_KEY:
        raise ValueError("Missing HUME_API_KEY in .env")

    try:
        with open(LETTER_PATH, "r", encoding="utf-8") as file:
            letter_text = file.read()

        print(f"[HUME] Speaking with emotion: {emotion}")

        headers = {
            "Authorization": f"Bearer {HUME_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "text": letter_text,
            "voice": "emma",
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

        if response.status_code != 200:
            print(f"[HUME] Failed: {response.status_code} — {response.text}")
            return

        fd, path = tempfile.mkstemp(suffix=".mp3")
        with os.fdopen(fd, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        playsound(path)
        os.remove(path)

    except FileNotFoundError:
        print(f"[ERROR] Letter file not found at: {LETTER_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed to play Easter egg: {e}")