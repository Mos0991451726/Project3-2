import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ollama
import chromadb
from config import settings

ollama_client = ollama.Client(host=settings.OLLAMA_HOST, timeout=300)
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PATH)

def get_query_embedding(query: str) -> list:
    result = ollama_client.embeddings(
        model="nomic-embed-text",
        prompt=query
    )
    return result["embedding"]

def retrieve(query: str) -> list:
    try:
        collection = chroma_client.get_collection(name=settings.CHROMA_COLLECTION)
    except Exception:
        return []

    embedding = get_query_embedding(query)

    source_limits = {
        "wiki": 2, "xau": 3, "gold": 3,
        "analysis": 3, "gdp": 1, "inflation": 1,
    }

    all_docs = []
    for source, n in source_limits.items():
        try:
            result = collection.query(
                query_embeddings=[embedding],
                n_results=n,
                where={"source": source}
            )
            all_docs.extend(result["documents"][0])
        except Exception:
            pass

    return all_docs

def ask(query: str) -> str:
    docs = retrieve(query)
    context = "\n".join(docs) if docs else "ไม่มีข้อมูลใน context"

    prompt = f"""คุณคือผู้เชี่ยวชาญด้านการลงทุนในทองคำ มีความรู้เกี่ยวกับ:
- ราคาทองคำและปัจจัยที่ส่งผล
- เศรษฐกิจโลก เช่น GDP อัตราเงินเฟ้อ
- ตลาดการเงิน เช่น ค่าเงินดอลลาร์ อัตราดอกเบี้ย
- การลงทุนในทองคำทั้งระยะสั้นและระยะยาว

กฎในการตอบ:
- ตอบเป็นภาษาไทยเสมอ
- ใช้ข้อมูลจาก context ที่ให้มา
- ถ้าไม่มีข้อมูลใน context ให้บอกว่าไม่มีข้อมูลในระบบ
- ห้ามทำนายราคาทองในอนาคต
- ห้ามแนะนำให้ซื้อหรือขายทองโดยตรง
- อธิบายให้เข้าใจง่าย

Context:
{context}

คำถาม: {query}

คำตอบ:"""

    try:
        response = ollama_client.generate(
            model="gpt-oss:20b",
            prompt=prompt,
        )
        return response["response"]
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"