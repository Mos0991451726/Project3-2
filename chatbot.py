import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ollama
import chromadb
from google import genai

# === Config ===
GEMINI_API_KEY = "AIzaSyBvEzmQUmVJvW3Vj4OyRm45aZH78QBUDkk"  # ใส่ API Key
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "gold_knowledge"

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
ollama_client = ollama.Client(host="http://26.46.48.83:11434")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

def get_query_embedding(query: str) -> list:
    result = ollama_client.embeddings(
        model="nomic-embed-text",
        prompt=query
    )
    return result["embedding"]

def retrieve(query: str) -> list:
    collection = chroma_client.get_collection(name=COLLECTION_NAME)
    embedding = get_query_embedding(query)
    
    # กำหนดจำนวนที่ดึงแต่ละ source ตามความสำคัญ
    source_limits = {
        "wiki": 2,
        "xau": 3,
        "gold": 3,
        "analysis": 3,
        "gdp": 1,
        "inflation": 1,
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
        except:
            pass
    
    return all_docs

def ask(query: str) -> str:
    # ดึง documents ที่เกี่ยวข้อง
    docs = retrieve(query)
    
    # print("\n=== Retrieved Documents ===")
    # for i, doc in enumerate(docs):
    #     print(f"[{i+1}] {doc[:100]}")
    # print("===========================\n")
    
    context = "\n".join(docs)
    
    prompt = f"""คุณคือผู้เชี่ยวชาญด้านการลงทุนในทองคำ มีความรู้เกี่ยวกับ:
- ราคาทองคำและปัจจัยที่ส่งผล
- เศรษฐกิจโลก เช่น GDP อัตราเงินเฟ้อ
- ตลาดการเงิน เช่น ค่าเงินดอลลาร์ (DXY) อัตราดอกเบี้ย ราคาน้ำมัน
- ความสัมพันธ์ระหว่างปัจจัยต่างๆ กับราคาทอง
- การลงทุนในทองคำทั้งระยะสั้นและระยะยาว

กฎในการตอบ:
- ตอบเป็นภาษาไทยเสมอ
- ใช้ข้อมูลจาก context ที่ให้มาในการตอบ
- ถ้าไม่มีข้อมูลใน context ให้บอกว่าไม่มีข้อมูลในระบบ
- ห้ามทำนายราคาทองในอนาคตโดยเด็ดขาด
- ห้ามแนะนำให้ซื้อหรือขายทองโดยตรง เพราะเป็นข้อมูลเพื่อการศึกษาเท่านั้น
- อธิบายให้เข้าใจง่าย ไม่ใช้ศัพท์เทคนิคมากเกินไป

Context:
{context}

คำถาม: {query}

คำตอบ:"""
    
    for attempt in range(3):  # retry 3 รอบ
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        
        except Exception as e:
            if "429" in str(e):  # rate limit
                wait = (attempt + 1) * 10
                print(f"Rate limit รอ {wait} วินาที...")
                time.sleep(wait)
            else:
                return f"เกิดข้อผิดพลาด: {str(e)}"
    
    return "ขออภัย ไม่สามารถตอบได้ในขณะนี้ กรุณาลองใหม่อีกครั้ง"

if __name__ == "__main__":
    print("Gold Chatbot ready! (พิมพ์ 'exit' เพื่อออก)")
    while True:
        query = input("\nคุณ: ")
        if query.lower() == "exit":
            break
        answer = ask(query)
        print(f"\nBot: {answer}")