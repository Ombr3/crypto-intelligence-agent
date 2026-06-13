import os
import chromadb
from chromadb.utils import embedding_functions

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"

def load_documents() -> list[dict]:
    """Load all .txt and .pdf text from the data/ folder"""
    docs = []
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            # Split into chunks by paragraph
            chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
            for i, chunk in enumerate(chunks):
                docs.append({
                    "id": f"{filename}_{i}",
                    "text": chunk,
                    "source": filename
                })
    return docs

def build_vector_store():
    """Embed documents and store in ChromaDB"""
    docs = load_documents()
    if not docs:
        print("No documents found in data/ folder")
        return

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    ef = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="crypto_knowledge",
        embedding_function=ef
    )

    collection.upsert(
        ids=[d["id"] for d in docs],
        documents=[d["text"] for d in docs],
        metadatas=[{"source": d["source"]} for d in docs]
    )
    print(f"Stored {len(docs)} chunks in vector store")

def retrieve(query: str, n_results: int = 3) -> list[str]:
    """Retrieve the most relevant chunks for a query"""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    ef = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="crypto_knowledge",
        embedding_function=ef
    )

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]

if __name__ == "__main__":
    build_vector_store()
    results = retrieve("What is funding rate?")
    print("\nRetrieved chunks:")
    for r in results:
        print(f"- {r}")
