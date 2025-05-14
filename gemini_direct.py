# gemini_direct.py

import requests

def run_gemini(prompt: str, api_key: str, model: str = "models/gemini-2.0-flash"):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        res.raise_for_status()
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"
