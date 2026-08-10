import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
load_dotenv(current_dir.parent / ".env")

URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_URL = "https://openrouter.ai/api/v1/embeddings"


def send_query(user_input: list[dict[str, Any]]):
    response = requests.post(
        url=URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        data=json.dumps(
            {
                "model": MODEL,
                "messages": [{"role": "user", "content": user_input}],
                "plugins": [
                    {
                        "id": "file-parser",
                        "pdf": {
                            "engine": "cloudflare-ai",
                        },
                    }
                ],
            }
        ),
    )

    return response.json()["choices"][0]["message"]["content"]


def get_embeddings(texts: list[str]) -> list[list[float]]:
    response = requests.post(
        url=EMBEDDING_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"model": EMBEDDING_MODEL, "input": texts}),
    )
    
    sorted_data = sorted(response.json()["data"], key=lambda x: x["index"])
    
    return [item["embedding"] for item in sorted_data]


if __name__ == "__main__":
    sample_text = """
    Sztuczna inteligencja (AI) oraz duże modele językowe (tzw. LLM) zrewolucjonizowały sposób, 
    w jaki wchodzimy w interakcję z maszynami. Jeszcze dekadę temu wygenerowanie płynnego, 
    sensownego tekstu przez komputer wydawało się mrzonką. Dzisiaj algorytmy są w stanie pisać eseje, 
    analizować dane i programować. Modele te uczą się na potężnych zbiorach danych, które obejmują 
    m.in. artykuły naukowe, książki oraz zasoby internetowe.
        
    Jednakże, mimo swojej imponującej wiedzy, modele językowe mają pewne fundamentalne ograniczenia. 
    Przede wszystkim nie posiadają one domyślnego dostępu do wiedzy w czasie rzeczywistym. 
    Mają również tendencję do tzw. halucynacji, czyli zmyślania faktów w bardzo przekonujący sposób. 
    Rozwiązaniem tego problemu jest architektura RAG (Retrieval-Augmented Generation). 
    Pozwala ona na dynamiczne przeszukiwanie zewnętrznych baz danych, np. dokumentów firmowych, 
    zanim model wygeneruje ostateczną odpowiedź dla użytkownika.
        
    W procesie tym kluczową rolę odgrywają wektorowe bazy danych, takie jak ChromaDB czy Qdrant. 
    Zanim jednak jakikolwiek tekst trafi do bazy, musi zostać starannie podzielony na mniejsze fragmenty. 
    Każdy taki fragment jest następnie zamieniany na ciąg liczb, czyli wektor osadzeń (embedding). 
    Dzięki temu, gdy użytkownik zadaje pytanie o godz. 14:30 dotyczące specyfikacji tajnego projektu, 
    system może błyskawicznie odnaleźć odpowiedni paragraf. To właśnie precyzyjne cięcie tekstu 
    gwarantuje, że model otrzyma właściwy kontekst i odpowie bezbłędnie.
    """

    result = get_embeddings(sample_text)
    print(len(result))
