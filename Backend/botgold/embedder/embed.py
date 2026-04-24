import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

import ollama
import chromadb
from converters.convert_gdp       import convert_gdp
from converters.convert_inflation import convert_inflation
from converters.convert_gold      import convert_gold
from converters.convert_xau       import convert_xau
from converters.convert_wiki      import convert_wiki
from converters.convert_analysis  import convert_analysis

# === Config จาก .env ===
CHROMA_PATH     = os.getenv("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "gold_knowledge")
OLLAMA_HOST     = os.getenv("OLLAMA_HOST", "http://localhost:11434")
BATCH_SIZE      = 100

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
ollama_client = ollama.Client(host=OLLAMA_HOST)

def get_embedding(texts: list) -> list:
    embeddings = []
    for text in texts:
        result = ollama_client.embeddings(
            model="nomic-embed-text",
            prompt=text
        )
        embeddings.append(result["embedding"])
    return embeddings

def embed_documents(documents: list, source: str, collection):
    print(f"\nEmbedding '{source}': {len(documents)} documents")
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

def embed_all(force: bool = False):
    # ถ้า force=True → ลบ collection เก่าก่อน
    if force:
        try:
            chroma_client.delete_collection(name=COLLECTION_NAME)
            print(f"🗑️  Deleted old collection '{COLLECTION_NAME}'")
        except Exception:
            pass

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    print(f"Collection '{COLLECTION_NAME}' has {collection.count()} documents")

    if collection.count() > 0 and not force:
        print("Already embedded. ใช้ --force เพื่อ embed ใหม่ทั้งหมด")
        return collection

    sources = {
        "gdp":       convert_gdp,
        "inflation": convert_inflation,
        "gold":      convert_gold,
        "xau":       convert_xau,
        "wiki":      convert_wiki,
        "analysis":  convert_analysis,
    }

    for source, converter in sources.items():
        try:
            docs = converter()
            if docs:
                embed_documents(docs, source, collection)
            else:
                print(f"⚠️  No documents from '{source}', skipping.")
        except Exception as e:
            print(f"❌ Error in '{source}': {e}")

    print(f"\n✅ Total embedded: {collection.count()} documents")
    return collection

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="ลบ collection เก่าแล้ว embed ใหม่")
    args = parser.parse_args()
    embed_all(force=args.force)