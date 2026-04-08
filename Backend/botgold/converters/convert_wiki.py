import os

SCRAPED_PATH = "./scraped"
CHUNK_SIZE = 500

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list:
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def convert_wiki():
    documents = []
    
    for filename in os.listdir(SCRAPED_PATH):
        if not filename.endswith(".txt"):
            continue
        
        filepath = os.path.join(SCRAPED_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        
        chunks = chunk_text(text)
        documents.extend(chunks)
        print(f"{filename}: {len(chunks)} chunks")
    
    return documents

if __name__ == "__main__":
    docs = convert_wiki()
    print(f"\nTotal documents: {len(docs)}")
    print("Example:")
    print(docs[0][:200])