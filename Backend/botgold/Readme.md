# Gold Knowledge Chatbot 🪙

Chatbot ให้ความรู้เกี่ยวกับทองคำ ราคาทอง และปัจจัยทางเศรษฐกิจที่เกี่ยวข้อง โดยใช้ RAG (Retrieval-Augmented Generation)

## Tech Stack
- **Embedding**: Ollama + nomic-embed-text
- **Vector DB**: ChromaDB
- **LLM**: Google Gemini
- **Data**: Kaggle Datasets + Wikipedia

## การติดตั้ง

### 1. Clone โปรเจค
```bash
git clone <repo url>
cd py
```

### 2. ติดตั้ง Library
```bash
pip install pandas kaggle beautifulsoup4 requests chromadb ollama google-genai
```

### 3. ตั้งค่า Kaggle
- โหลด `kaggle.json` จาก [kaggle.com](https://www.kaggle.com) → Account → API → Create New Token
- วางไว้ที่:
  - Windows: `C:\Users\<username>\.kaggle\kaggle.json`
  - Mac/Linux: `~/.kaggle/kaggle.json`

### 4. ตั้งค่า API Key
เปิดไฟล์ `embedder/embed.py` และ `chatbot.py` แล้วใส่ Gemini API Key:
```python
GEMINI_API_KEY = "your-api-key-here"
```
> โหลด API Key ได้จาก [Google AI Studio](https://aistudio.google.com)

### 5. ติดตั้ง Ollama
- โหลดจาก [ollama.com](https://ollama.com/download)
- โหลด embedding model:
```bash
ollama pull nomic-embed-text
```

## การใช้งาน

### ขั้นตอนที่ 1 — โหลดและ Clean Data
```bash
python main.py
```

### ขั้นตอนที่ 2 — Scrape ข้อมูล Wikipedia
```bash
python -m scrapers.scrape_wiki
```

### ขั้นตอนที่ 3 — Embed ข้อมูล
```bash
python -m embedder.embed
```
> ⚠️ ต้องเปิด Ollama ค้างไว้ระหว่าง embed

### ขั้นตอนที่ 4 — รัน Chatbot
```bash
python chatbot.py
```

## โครงสร้างโปรเจค
```
project/
├── main.py                 ← รันทุกอย่าง
├── downloader.py           ← โหลด dataset จาก Kaggle
├── chatbot.py              ← RAG Chatbot
├── cleaners/               ← Clean แต่ละ dataset
│   ├── clean_gdp.py
│   ├── clean_inflation.py
│   ├── clean_gold.py
│   └── clean_xau.py
├── converters/             ← แปลง dataset เป็น text
│   ├── convert_gdp.py
│   ├── convert_inflation.py
│   ├── convert_gold.py
│   ├── convert_xau.py
│   ├── convert_wiki.py
│   └── convert_analysis.py
├── embedder/               ← Embed และเก็บใน ChromaDB
│   └── embed.py
└── scrapers/               ← Scrape Wikipedia
    └── scrape_wiki.py
```

## Dataset ที่ใช้
| Dataset | แหล่งข้อมูล |
|---|---|
| Global GDP per Capita 1960-Present | Kaggle |
| Global Inflation Rate 1960-Present | Kaggle |
| Gold Price and Relevant Metrics | Kaggle |
| XAUUSD Gold Price Historical Data 2004-2024 | Kaggle |
| Gold, XAU, Gold as an Investment | Wikipedia |

## ข้อควรระวัง
- Chatbot นี้ให้ข้อมูลเพื่อการศึกษาเท่านั้น
- ไม่แนะนำให้ซื้อหรือขายทองโดยตรง
- ไม่ทำนายราคาทองในอนาคต