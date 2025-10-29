import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load key and endpoint
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-5",  # model from OpenRouter
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

def load_badwords():
    with open("badwords.txt", "r") as f:
        return set(line.strip().lower() for line in f.readlines())

BADWORDS = load_badwords()

def filter_bad_words(text):
    words = text.lower().split()
    filtered_words = ["****" if w in BADWORDS else w for w in words]
    return " ".join(filtered_words)
