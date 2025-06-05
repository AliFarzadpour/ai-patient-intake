import streamlit as st
import openai
import tempfile
import os

st.set_page_config(page_title="AI Intake Chat", layout="centered")
st.title("🗣️ AI Medical Intake Chat (Voice + Text)")

openai.api_key = st.secrets["OPENAI_API_KEY"]

questions = [
    "What is your full name?",
    "What is your date of birth?",
    "What is the reason for your visit today?",
    "Do you have any allergies?",
    "Are you currently taking any medications?"
]

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []

def transcribe_audio(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name
    with st.spinner("Transcribing..."):
        result = openai.Audio.transcribe("whisper-1", open(tmp_path, "rb"))
    os.remove(tmp_path)
    return result["text"]

if st.session_state.step < len(questions):
    current_q = questions[st.session_state.step]
    st.markdown(f"**{current_q}**")

    col1, col2 = st.columns([2, 1])
    with col1:
        text_input = st.text_input("Type your answer:", key="text_input")
    with col2:
        audio_input = st.file_uploader("Or upload audio", type=["m4a", "mp3", "wav"], key="audio_input")

    final_answer = None

    if audio_input is not None:
        try:
            final_answer = transcribe_audio(audio_input)
            st.success("✅ Transcription complete")
            st.write(f"**You said:** {final_answer}")
        except Exception as e:
            st.error(f"Error transcribing audio: {e}")
    elif text_input:
        final_answer = text_input

    if final_answer:
        st.session_state.answers.append((current_q, final_answer))
        st.session_state.step += 1
        st.experimental_rerun()
else:
    st.success("✅ Intake Complete! Here's a summary:")
    for q, a in st.session_state.answers:
        st.write(f"**{q}**")
        st.write(f"{a}")
