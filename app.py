import streamlit as st
import openai
import tempfile
import os

# Title
st.set_page_config(page_title="AI Patient Intake", layout="centered")
st.title("🩺 AI Patient Intake Assistant")

# Get API Key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Basic patient info fields
questions = [
    "What is your full name?",
    "What is your date of birth?",
    "What is the reason for your visit today?",
    "Do you have any allergies?",
    "Are you currently taking any medications?"
]

# Initialize session state
if "responses" not in st.session_state:
    st.session_state.responses = {}

# Function to transcribe audio with Whisper API
def transcribe_audio(file_path):
    audio_file = open(file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

st.markdown("Please answer the following questions by typing or recording your voice.")

for q in questions:
    st.subheader(q)
    col1, col2 = st.columns([3, 1])
    with col1:
        text = st.text_input(f"Type your answer for: {q}", key=q)
    with col2:
        audio_file = st.file_uploader(f"Or upload audio for: {q}", type=["mp3", "m4a", "wav"], key=q+"_audio")
        if audio_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            with st.spinner("Transcribing..."):
                transcription = transcribe_audio(tmp_path)
                text = transcription
                st.success("Transcription complete.")
            os.remove(tmp_path)
    if text:
        st.session_state.responses[q] = text

# Display collected information
if len(st.session_state.responses) == len(questions):
    st.markdown("---")
    st.success("✅ All information collected successfully.")
    st.header("📋 Patient Summary")
    for q, a in st.session_state.responses.items():
        st.write(f"**{q}**")
        st.write(f"{a}")
