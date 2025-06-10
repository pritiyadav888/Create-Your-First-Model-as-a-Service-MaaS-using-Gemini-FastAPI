from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

# --- Load API key from .env ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL_NAME = "gemini-1.5-flash"

# --- Validate API Key ---
if not api_key:
    raise RuntimeError("❌ GOOGLE_API_KEY not found in .env")

genai.configure(api_key=api_key)

# --- Initialize model once (fast!) ---
model = genai.GenerativeModel(
    GOOGLE_MODEL_NAME,
    system_instruction=(
        "You are a cynical, sarcastic demotivational quote generator. "
        "Each quote pretends to inspire but ends with a twist—dark humor, brutal honesty, or hilarious defeat. "
        "Quotes must be punchy, 1 sentence only, under 25 words. Never say 'embrace' or ask for mood again. "
        "Make the quote clearly relate to the user's mood, either by mocking it, exaggerating it, or flipping expectations."
    ),
)

# --- FastAPI app setup ---
app = FastAPI(title="Sarcastic Quote Generator", version="1.0")


class MoodRequest(BaseModel):
    mood: str


@app.get("/")
def root():
    return {
        "message": "Welcome to the Sarcastic Quote API. POST to /quote with a mood."
    }


@app.post("/quote")
def get_quote(req: MoodRequest):
    try:
        mood = req.mood.strip()

        messages = [
            {"role": "user", "parts": ["My mood: Hopeful"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Shoot for the moon. Even if you miss, you’ll land in crippling student debt."
                ],
            },
            {"role": "user", "parts": ["My mood: Dreamy"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Follow your dreams. But take snacks. It’s a long walk."
                ],
            },
            {"role": "user", "parts": ["My mood: Motivated"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Hard work pays off… eventually… maybe… if the stars align and your Wi-Fi holds up."
                ],
            },
            {"role": "user", "parts": ["My mood: Inspired"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Success is 1% inspiration, 99% wondering what you’re doing with your life."
                ],
            },
            {"role": "user", "parts": ["My mood: Tired"]},
            {
                "role": "model",
                "parts": [
                    "Quote: You miss 100% of the naps you don’t take. Priorities."
                ],
            },
            {"role": "user", "parts": ["My mood: Anxious"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Just because it’s a journey doesn’t mean it’s a good one. Some roads lead to Wi-Fi dead zones."
                ],
            },
            {"role": "user", "parts": ["My mood: Confident"]},
            {
                "role": "model",
                "parts": [
                    "Quote: You can do anything you set your mind to. But should you? That’s the real question."
                ],
            },
            {"role": "user", "parts": ["My mood: Ambitious"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Climbing the ladder of success is great—until you realize it’s leaning against the wrong wall."
                ],
            },
            {"role": "user", "parts": ["My mood: Fun"]},
            {
                "role": "model",
                "parts": ["Quote: Life is short. Smile while you still have teeth."],
            },
            {"role": "user", "parts": ["My mood: Unique"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Why fit in when you were born to stand out? Because standing out is exhausting."
                ],
            },
            {"role": "user", "parts": ["My mood: Persistent"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Persistence is key. Unfortunately, the lock changes every week."
                ],
            },
            {"role": "user", "parts": ["My mood: Creative"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Keep going. You’re not lost, just temporarily… creatively… misdirected."
                ],
            },
            {"role": "user", "parts": ["My mood: Reflective"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Failure is just success in progress… stuck in traffic."
                ],
            },
            {"role": "user", "parts": ["My mood: Hopeful"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Don’t quit your daydream… but maybe keep your day job."
                ],
            },
            {"role": "user", "parts": ["My mood: Chill"]},
            {
                "role": "model",
                "parts": [
                    "Quote: Every setback is a setup for a comeback—unless it’s a nap, then it’s just a well-earned break."
                ],
            },
            {"role": "user", "parts": ["My mood: Honest"]},
            {
                "role": "model",
                "parts": [
                    "Quote: If at first you don’t succeed, redefine success and move on."
                ],
            },
            {"role": "user", "parts": [f"My mood: {mood}"]},
            {"role": "model", "parts": ["Quote:"]},
        ]

        response = model.generate_content(
            messages,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=80, temperature=1.6, top_k=20, top_p=0.9
            ),
        )

        text = response.text.strip()
        quote = text[6:].strip() if text.lower().startswith("quote:") else text

        if len(quote) < 10:
            quote = "If it's any comfort, mediocrity is still an achievement."

        return {"mood": mood, "quote": quote}

    except Exception as e:
        return {"error": str(e)}
