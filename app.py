import streamlit as st
import openai

st.set_page_config(page_title="AI Intake Chat", layout="centered")
st.title("🗣️ AI Medical Intake Chat")

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

if st.session_state.step < len(questions):
    current_q = questions[st.session_state.step]
    st.markdown(f"**{current_q}**")
    user_input = st.text_input("Your answer:", key="user_input")

    if user_input:
        st.session_state.answers.append((current_q, user_input))
        st.session_state.step += 1
        st.experimental_rerun()
else:
    st.success("✅ Intake Complete! Here's a summary:")
    for q, a in st.session_state.answers:
        st.write(f"**{q}**")
        st.write(f"{a}")

