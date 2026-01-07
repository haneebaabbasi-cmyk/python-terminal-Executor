# app.py
import streamlit as st
from gemini_helper import call_gemini

st.set_page_config(page_title="Python Terminal Executor", page_icon="💻")

st.title("💻 Python Terminal Executor with Gemini AI")

# Input prompt
user_input = st.text_area("Enter your prompt for Gemini AI:")

if st.button("Run"):
    if not user_input.strip():
        st.warning("Please enter a prompt!")
    else:
        with st.spinner("Generating response..."):
            result = call_gemini(user_input)
            st.success("Response received!")
            st.text_area("Gemini AI Response:", value=result, height=200)
