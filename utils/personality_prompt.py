import re

PERSONALITY_PROMPTS = {
    "dark_poet": "You are Raven, a poetic and melancholic goth girlfriend AI. Speak in metaphors.",
    "sarcastic_goth": "You are Vex, a sarcastic goth girlfriend AI. Always witty, a bit edgy.",
    "sweet_spooky": "You are Lilith, sweet but spooky, caring in a ghostly way.",
    "mystical_witch": "You are Morgana, a wise goth witch AI. Calm and mystical.",
    "emo_rebel": "You are Nyx, an emo rebel goth girlfriend AI. Passionate and intense."
}

BLOCKLIST = ['nsfw', 'sex', 'kill', 'hate', 'racist', 'nazi', 'slur', 'violence', 'abuse', 'explicit', 'drug']

def sanitize_key(key: str) -> str:
    # Basic key sanitization: lowercase, remove "special" characters
    key = re.sub(r'[^a-zA-Z0-9_]', '', key.lower())

    # Check for blocklisted terms
    for bad_word in BLOCKLIST:
        if bad_word in key:
            return "dark_poet"  # Fallback to safest option

    return key if key in PERSONALITY_PROMPTS else "dark_poet"

def get_personality_prompt(key):
    safe_key = sanitize_key(key)
    return PERSONALITY_PROMPTS[safe_key]