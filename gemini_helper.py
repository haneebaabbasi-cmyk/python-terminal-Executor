# gemini_helper.py
# Updated import for Google Gemini / GenAI

import os
from google import genai

# Initialize the client
client = genai.Client()  # Make sure your API key is set in environment variables

def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini AI and returns the response.
    """
    response = client.generate_text(prompt=prompt)
    return response.text
