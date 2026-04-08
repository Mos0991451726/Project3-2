import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ollama
import chromadb
from converters.convert_gdp import convert_gdp
from converters.convert_inflation import convert_inflation
from converters.convert_gold import convert_gold
from converters.convert_xau import convert_xau
from converters.convert_wiki import convert_wiki
from converters.convert_analysis import convert_analysis

# === Config ===
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "gold_knowledge"
BATCH_SIZE = 100

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

client = ollama.Client(host="http://26.46.48.83:11434")

def get_embedding(texts: list) -> list:
    embeddings = []
    for text in texts:
        result = client.embeddings(
            model="nomic-embed-text",
            prompt=text
        )
        embeddings.append(result["embedding"])
    return embeddings

def embed_documents(documents: list, source: str, collection):
    print(f"\nEmbedding {source}: {len(documents)} documents")
    
    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i:i + BATCH_SIZE]
        embeddings = get_embedding(batch)
        
        collection.add(
            documents=batch,
            embeddings=embeddings,
            ids=[f"{source}_{i+j}" for j in range(len(batch))],
            metadatas=[{"source": source} for _ in batch]
        )
        print(f"  {min(i + BATCH_SIZE, len(documents))}/{len(documents)} done")

def embed_all():
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    
    print(f"Collection '{COLLECTION_NAME}' has {collection.count()} documents")
    
    if collection.count() > 0:
        print("Already embedded, skipping.")
        return collection
    
    sources = {
        "gdp": convert_gdp(),
        "inflation": convert_inflation(),
        "gold": convert_gold(),
        "xau": convert_xau(),
        "wiki": convert_wiki(),
        "analysis": convert_analysis(),
    }
    
    for source, documents in sources.items():
        embed_documents(documents, source, collection)
    
    print(f"\nTotal embedded: {collection.count()} documents")
    return collection

if __name__ == "__main__":
    embed_all()