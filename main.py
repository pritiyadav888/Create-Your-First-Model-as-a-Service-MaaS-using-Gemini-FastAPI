# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

from prompts import FEW_SHOT_EXAMPLES, SYSTEM_PROMPT

# --- Load API key securely from .env ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL_NAME = "gemini-1.5-flash"

# --- Validate presence of API key ---
if not api_key:
    raise RuntimeError("❌ GOOGLE_API_KEY not found in .env file")

# --- Configure Gemini with API key ---
genai.configure(api_key=api_key)

# --- Initialize Gemini model with system instruction ---
model = genai.GenerativeModel(
    GOOGLE_MODEL_NAME,
    system_instruction=SYSTEM_PROMPT,
)

# --- Define FastAPI app ---
app = FastAPI(title="Sarcastic Quote Generator", version="1.0")


# --- Define input schema ---
class MoodRequest(BaseModel):
    mood: str


# --- Root endpoint for basic check ---
@app.get("/")
def root():
    return {
        "message": "Welcome to the Sarcastic Quote API. POST to /quote with a mood."
    }


# --- POST endpoint to generate sarcastic quote ---
@app.post("/quote")
def get_quote(req: MoodRequest):
    try:
        mood = req.mood.strip()
        if not mood:
            return {"error": "Mood cannot be empty."}

        # Build conversation history with few-shot examples
        messages = FEW_SHOT_EXAMPLES + [
            {"role": "user", "parts": [f"My mood: {mood}"]},
            {"role": "model", "parts": ["Quote:"]},
        ]

        # Generate content using Gemini
        response = model.generate_content(
            messages,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=80,
                temperature=1.6,
                top_k=20,
                top_p=0.9,
            ),
        )

        # Post-process quote
        text = response.text.strip()
        quote = text[6:].strip() if text.lower().startswith("quote:") else text

        if len(quote) < 10:
            quote = "If it's any comfort, mediocrity is still an achievement."

        return {"mood": mood, "quote": quote}

    except Exception as e:
        return {"error": str(e)}
