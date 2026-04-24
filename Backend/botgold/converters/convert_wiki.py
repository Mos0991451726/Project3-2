import os

CLEANED_PATH = "./scraped/cleaned"
CHUNK_SIZE   = 500   # words per chunk
MIN_WORDS    = 50    # ตัด chunk ที่สั้นเกินออก

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list:
    words  = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        # ตัด chunk ที่สั้นเกิน (noise)
        if len(chunk.split()) >= MIN_WORDS:
            chunks.append(chunk.strip())
    return chunks

def convert_wiki() -> list:
    documents = []

    if not os.path.exists(CLEANED_PATH):
        print(f"⚠️  ไม่พบ {CLEANED_PATH} กรุณารัน clean_wiki() ก่อน")
        return documents

    for filename in sorted(os.listdir(CLEANED_PATH)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(CLEANED_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        documents.extend(chunks)
        print(f"{filename}: {len(chunks)} chunks")

    print(f"Wiki total: {len(documents)} chunks")
    return documents

if __name__ == "__main__":
    docs = convert_wiki()
    print(f"\nTotal: {len(docs)}")
    if docs:
        print("Example:")
        print(docs[0][:300])
