import uuid
from pathlib import Path

import chromadb

from .indexing import chunk_text
from .openrouter import get_embeddings

chroma_dir = Path(__file__).resolve().parent.parent / ".chroma"
client = chromadb.PersistentClient(chroma_dir)
collection = client.get_or_create_collection(name="main")


def add_to_collection(text: str, filename: str) -> str:
    """
    Divides text into chunks, generates embeddings and metadata
    and adds it to a collection.

    Args:
        text (str): text to chunk and add to collection
        filename (str): file's name

    Returns:
        str: returns file's uuid
    """

    chunks = chunk_text(text)

    ids = []
    metadatas = []

    file_uuid = str(uuid.uuid4())[:8]
    embeddings = get_embeddings(chunks)

    for i, _ in enumerate(chunks):
        chunk_id = f"{file_uuid}_chunk_{i}"

        ids.append(chunk_id)
        metadatas.append(
            {"filename": filename, "chunk_index": i, "file_uuid": file_uuid}
        )

    collection.add(
        ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas
    )

    return file_uuid


def retrieve_chunks(query: str, n_results: int = 4) -> list[dict[str, any]]:
    """
    Takes a query, generates an embedding for it and searches
    the vector database with this embedding.

    Args:
        query (str): a query for searching the database
        n_results (int): number of chunks to retrieve

    Returns:
        list[dict[str, any]]: returns list of dictionaries with results
    """

    query_vector = get_embeddings([query])
    results = collection.query(query_embeddings=query_vector, n_results=n_results)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted_results = []
    for doc, meta, distance in zip(documents, metadatas, distances):
        formatted_results.append({"text": doc, "metadata": meta, "distance": distance})

    return formatted_results


if __name__ == "__main__":
    query = "Czym jest architektura RAG i jakie problemy rozwiązuje?"

    found = retrieve_chunks(query)
    for i, result in enumerate(found, 1):
        print(f"\n Result: {i} | Distance: {result['distance']:.4f}")
        print(f"File: {result['metadata']['filename']} | Chunk: {result['metadata']['chunk_index']}")
        print(f"Text: {result['text'][:150]}")
