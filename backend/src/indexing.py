from llama_index.core.node_parser import SentenceSplitter


def chunk_text(text: str, chunk_size: int = 512, chunk_overlap: int = 100) -> list[str]:
    """
    Takes raw text and divides it in small overlapping fragments.

    Args:
        text (str): raw text to divide
        chunk_size (int): maximum number of tokens in one fragment
        chunk_overlap (int): number of overlapping tokens between fragments

    Returns:
        list[str]: list of clean text chunks
    """

    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    chunks = splitter.split_text(text)

    return chunks


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

    result_chunks = chunk_text(sample_text)

    for i, chunk in enumerate(result_chunks):
        print(f"Chunk {i + 1}: {chunk}")
