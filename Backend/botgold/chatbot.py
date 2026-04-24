import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ollama
import chromadb
import requests
import yfinance as yf
from config import settings
import google.generativeai as genai

ollama_client = ollama.Client(host=settings.OLLAMA_HOST, timeout=300)
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PATH)

genai.configure(api_key=settings.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# ─── Real-time Data ───

def get_gold_price() -> str:
    """ดึงราคาทองจาก Gold API (XAU/THB) และคำนวณราคาทองไทย"""
    try:
        res = requests.get(
            "https://www.goldapi.io/api/XAU/THB",
            headers={"x-access-token": settings.GOLD_API_KEY},
            timeout=5
        )
        data = res.json()

        price      = data.get("price", 0)
        open_p     = data.get("open_price", 0)
        high       = data.get("high_price", 0)
        low        = data.get("low_price", 0)
        change     = data.get("ch", 0)
        change_pct = data.get("chp", 0)
        g24k       = data.get("price_gram_24k", 0)
        g22k       = data.get("price_gram_22k", 0)
        g18k       = data.get("price_gram_18k", 0)

        # คำนวณราคาทองไทย (1 บาททอง = 15.244 กรัม)
        baht_weight    = 15.244
        gold_baht_sell = g24k * baht_weight
        gold_baht_buy  = gold_baht_sell - 200
        gold_roop_sell = gold_baht_sell + 700
        gold_roop_buy  = gold_baht_sell - 800

        return f"""ราคาทองคำไทย (ประมาณการ):

ทองคำแท่ง:
- รับซื้อ: {gold_baht_buy:,.2f} บาท
- ขายออก: {gold_baht_sell:,.2f} บาท

ทองรูปพรรณ:
- รับซื้อ: {gold_roop_buy:,.2f} บาท
- ขายออก: {gold_roop_sell:,.2f} บาท

ราคาทองโลก (XAU/THB):
- ปัจจุบัน: {price:,.2f} บาท/ออนซ์
- เปิด: {open_p:,.2f} | สูงสุด: {high:,.2f} | ต่ำสุด: {low:,.2f}
- เปลี่ยนแปลง: {change:+.2f} บาท ({change_pct:+.2f}%)

ราคาต่อกรัม:
- ทอง 24K: {g24k:,.2f} บาท/กรัม
- ทอง 22K: {g22k:,.2f} บาท/กรัม
- ทอง 18K: {g18k:,.2f} บาท/กรัม

หมายเหตุ: ราคาทองไทยเป็นการประมาณการ ราคาจริงอาจแตกต่างตามแต่ละร้านค้า"""

    except Exception as e:
        return f"ไม่สามารถดึงราคาทองได้: {e}"

def get_indicators() -> str:
    """ดึง indicators จาก yfinance"""
    try:
        tickers = yf.Tickers("DX-Y.NYB ^VIX CL=F ^TNX")
        dxy   = tickers.tickers["DX-Y.NYB"].fast_info["last_price"]
        vix   = tickers.tickers["^VIX"].fast_info["last_price"]
        oil   = tickers.tickers["CL=F"].fast_info["last_price"]
        us10y = tickers.tickers["^TNX"].fast_info["last_price"]

        return f"""Indicators ปัจจุบัน:
- DXY (ดัชนีดอลลาร์): {dxy:.2f} (สูง = ดอลลาร์แข็ง = ทองมักลง)
- VIX (ความกลัวตลาด): {vix:.2f} (สูง = ตลาดกลัว = ทองมักขึ้น)
- น้ำมันดิบ WTI: {oil:.2f} USD/barrel
- อัตราดอกเบี้ย US 10Y: {us10y:.2f}%"""

    except Exception as e:
        return f"ไม่สามารถดึง indicators ได้: {e}"

def get_realtime_context() -> str:
    gold  = get_gold_price()
    indic = get_indicators()
    return f"{gold}\n\n{indic}"

# ─── เช็คว่าถามเรื่องอดีตหรือเปล่า → ถ้าใช่ไม่ต้องดึง real-time ───

HISTORY_KEYWORDS = [
    "ปี 20", "ปี 19", "ในอดีต", "ที่ผ่านมา", "ย้อนหลัง",
    "เคย", "ตอนนั้น", "ช่วงนั้น", "สมัย", "แต่ก่อน",
    "ประวัติ", "historical", "in the past", "previously",
    "ในช่วง", "ตลอด", "ระหว่างปี",
]

# คำที่ต้องดึง real-time เฉพาะเจาะจง (ไม่ใช้คำกว้าง เช่น "ราคาทอง")
PRICE_KEYWORDS = [
    "ราคาทองวันนี้", "ราคาทองตอนนี้", "ราคาทองปัจจุบัน",
    "ทองราคาเท่าไหร่", "ทองราคาเท่าไร", "ราคาทองล่าสุด",
    "ราคาล่าสุด", "ทองไทย", "ราคาปัจจุบัน", "วันนี้ราคา",
    "ทองแท่ง", "ทองรูปพรรณ", "gold price today",
    "dxy ตอนนี้", "vix ตอนนี้", "indicators ตอนนี้",
    "ค่าเงินดอลลาร์ตอนนี้", "น้ำมันวันนี้",
]

def needs_realtime(query: str) -> bool:
    q = query.lower()
    # ถ้ามีคำที่บ่งบอกว่าถามอดีต → ไม่ดึง real-time
    if any(kw in q for kw in HISTORY_KEYWORDS):
        return False
    return any(kw in q for kw in PRICE_KEYWORDS)

# ─── RAG ───

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
    "wiki":     2,
    "xau":      8,  
    "gold":     5,   
    "analysis": 5,   
    "gdp":      2,   
    "inflation": 2,  
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

# ─── Main ───

def ask(query: str, history: list = []) -> str:
    docs = retrieve(query)
    rag_context = "\n".join(docs) if docs else "ไม่มีข้อมูลใน context"

    realtime_text = ""
    if needs_realtime(query):
        realtime_text = f"\nข้อมูล Real-time ล่าสุด:\n{get_realtime_context()}\n"

    history_text = ""
    if history:
        history_text = "บทสนทนาก่อนหน้า:\n"
        for msg in history:
            role = "ผู้ใช้" if msg["role"] == "user" else "แชทบอท"
            history_text += f"{role}: {msg['content']}\n"
        history_text += "\n"

    prompt = f"""คุณคือผู้เชี่ยวชาญด้านการลงทุนในทองคำ มีความรู้เกี่ยวกับ:
- ราคาทองคำและปัจจัยที่ส่งผล
- เศรษฐกิจโลก เช่น GDP อัตราเงินเฟ้อ
- ตลาดการเงิน เช่น ค่าเงินดอลลาร์ อัตราดอกเบี้ย
- การลงทุนในทองคำทั้งระยะสั้นและระยะยาว

กฎในการตอบ:
- ตอบเป็นภาษาไทยเสมอ
- ใช้ข้อมูลจาก context และ real-time data ที่ให้มา
- ถ้าไม่มีข้อมูลใน context ให้บอกว่าไม่มีข้อมูลในระบบ
- ห้ามทำนายราคาทองในอนาคต
- ห้ามแนะนำให้ซื้อหรือขายทองโดยตรง
- อธิบายให้เข้าใจง่าย
- ห้ามใช้ Markdown เช่น **, ##, ||, --- เด็ดขาด
- ตอบเป็นข้อความธรรมดา จัดย่อหน้าให้อ่านง่าย
- แบ่งหัวข้อด้วยการขึ้นบรรทัดใหม่และใช้ หมายเลข 1. 2. 3. แทน
- ถ้าถามราคาทองไทยให้แสดงทั้งทองคำแท่งและทองรูปพรรณ พร้อมราคารับซื้อและขายออก
- ถ้ามีบทสนทนาก่อนหน้า ให้คุยต่อจากเรื่องเดิมได้เลย
{realtime_text}
{history_text}Context จาก RAG:
{rag_context}

คำถามปัจจุบัน: {query}

คำตอบ:"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"