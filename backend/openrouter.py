import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
load_dotenv(current_dir.parent / '.env')

URL="https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL")

def send_query(user_input: str):
    response = requests.post(
        url = URL,
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        data = json.dumps({
            "model": MODEL,
            "messages": [ {
                "role": "user",
                "content": user_input
            } ]   
        })
    )
    print(response.json())
    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    result = send_query("hello")
    print(result)