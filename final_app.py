import streamlit as st
import uuid
import os
from dotenv import load_dotenv
from utils.firebase_utils import get_user_terms_acceptance, set_user_terms_acceptance, save_user_interaction
from utils.personality_prompt import get_personality_prompt, PERSONALITY_PROMPTS
from utils.expression_utils import speak
from easter_egg import play_easter_egg
import cohere

# Load environment variables
load_dotenv()

# Initialize Cohere
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
    st.session_state.personality = "dark_poet"
    st.session_state.messages = []

st.title("🖤 Goth Girlfriend AI")
st.subheader(f"Personality: {st.session_state.personality}")

# Terms Agreement
if not get_user_terms_acceptance(st.session_state.user_id):
    with open("terms_and_conditions.txt", "r") as terms:
            st.text(terms.read())
    if st.button("Accept Terms to Start Chatting"):
        set_user_terms_acceptance(st.session_state.user_id, True)
        st.rerun()
    else:
        st.warning("Please accept the terms to continue.")
        st.stop()

# Sidebar for personality change
with st.sidebar:
    st.markdown("### 🧠 Choose Personality")
    new_personality = st.selectbox("Personality", list(PERSONALITY_PROMPTS.keys()))
    if st.button("Set Personality"):
        st.session_state.personality = new_personality
        st.rerun()

# Chat Interface
user_text = st.text_input("You:", key="user_input")

if st.button("Send") and user_text:
    # Check for easter egg trigger
    if "23" in user_text.lower():
        st.info("💌 Easter Egg Triggered")
        play_easter_egg()
    else:
        # Save user interaction
        save_user_interaction(st.session_state.user_id, {"user": user_text})
        
        # Get personality prompt
        persona = get_personality_prompt(st.session_state.personality)
        
        # Get recent interactions for context
        from utils.firebase_utils import get_recent_interactions
        recent_interactions = get_recent_interactions(st.session_state.user_id)
        fewshot = "\n".join([f"User: {ex['user']}\nGothGirl: {ex.get('bot', '')}" 
                            for ex in recent_interactions if 'user' in ex])
        
        # Construct prompt
        final_prompt = f"{persona}\n\n{fewshot}\nUser: {user_text}\nGothGirl:"
        
        # Generate response
        response = co.generate(
            model="command-r-plus",
            prompt=final_prompt,
            max_tokens=200,
            temperature=0.8
        )
        
        reply = response.generations[0].text.strip()
        
        # Save and display response
        st.session_state.messages.append((user_text, reply))
        save_user_interaction(st.session_state.user_id, {"bot": reply})
        
        # Speak the response
        emotion_map = {
            "dark_poet": "sad",
            "sarcastic_goth": "angry",
            "sweet_spooky": "affectionate",
            "mystical_witch": "calm",
            "emo_rebel": "excited"
        }
        speak(reply, emotion=emotion_map.get(st.session_state.personality, "neutral"))

# Display Chat History
for user_msg, bot_msg in reversed(st.session_state.messages):
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Pookie:** {bot_msg}")
