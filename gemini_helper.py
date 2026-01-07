import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini 2.5 Flash and returns the response text.
    """
    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
    )

    text = ""
    for candidate in response.candidates:
        for part in candidate.content.parts:
            text += part.text
    return text
