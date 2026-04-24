# 🪙 แชทบอททองคำ (Gold Chatbot)

ระบบแชทบอทให้ความรู้ด้านการลงทุนทองคำ โดยใช้ RAG (Retrieval-Augmented Generation) ดึงข้อมูลจาก ChromaDB แล้วตอบด้วย LLM ผ่าน Ollama

---

## 🏗️ Tech Stack

| ส่วน | เทคโนโลยี |
|------|-----------|
| Frontend | React 18, React Router v6 |
| Backend API | FastAPI, Python 3.10+ |
| Database | MongoDB Atlas |
| Vector DB | ChromaDB |
| Embedding | Ollama + nomic-embed-text |
| LLM | Ollama (llama3.2 / gpt-oss:20b) |
| Auth | JWT + bcrypt |

---

## 📁 โครงสร้างโปรเจค

```
Final-Project/
├── Frontend/
│   └── goldbot/              ← React App
│       ├── src/
│       │   ├── api.js        ← เรียก Backend API
│       │   ├── App.jsx       ← หน้าหลัก Chat
│       │   ├── pages/
│       │   │   ├── Login.jsx
│       │   │   └── Register.jsx
│       │   └── components/
│       │       ├── Sidebar.jsx
│       │       ├── Message.jsx
│       │       ├── SettingsModal.jsx
│       │       └── ShareModal.jsx
│       └── .env              ← REACT_APP_API_URL
│
└── Backend/
    └── botgold/              ← FastAPI + RAG Bot
        ├── app.py            ← Entry point
        ├── config.py         ← อ่านค่าจาก .env
        ├── database.py       ← MongoDB connection
        ├── models.py         ← Pydantic schemas
        ├── auth.py           ← JWT authentication
        ├── chatbot.py        ← RAG engine
        ├── routers/
        │   ├── auth_router.py
        │   └── chat_router.py
        ├── cleaners/         ← Clean raw data
        ├── converters/       ← แปลง data เป็น text
        ├── embedder/
        │   └── embed.py      ← Embed ลง ChromaDB
        ├── scrapers/
        │   └── scrape_wiki.py
        ├── data/             ← Raw datasets (git ignore)
        ├── chroma_db/        ← Vector DB (git ignore)
        ├── requirements.txt
        └── .env              ← API Keys (git ignore)
```

> ⚠️ **หมายเหตุ:** ไฟล์ `chroma_db/` และ `data/` ไม่ได้อยู่ใน repository เพราะขนาดใหญ่เกินไป
> ต้องทำขั้นตอน Embed ข้อมูลใหม่เอง (ดูขั้นตอนที่ 5)

---

## ✅ สิ่งที่ต้องติดตั้งก่อน

| โปรแกรม | ดาวน์โหลด | หมายเหตุ |
|---------|-----------|---------|
| Node.js (LTS) | https://nodejs.org | สำหรับ Frontend |
| Python 3.10+ | https://python.org | สำหรับ Backend |
| Ollama | https://ollama.com/download | สำหรับ LLM + Embedding |

---

## 🚀 วิธีติดตั้งตั้งแต่ต้น

### ขั้นตอนที่ 1 — Clone โปรเจค

```bash
git clone <repo-url>
cd Final-Project
```

---

### ขั้นตอนที่ 2 — ตั้งค่า MongoDB Atlas

> ⚠️ โปรเจคนี้ใช้ MongoDB Atlas (cloud) ต้องตั้งค่าก่อนรัน Backend

**2.1 สมัครและสร้าง Cluster:**
1. ไปที่ https://cloud.mongodb.com → สมัครบัญชีฟรี
2. กด **"Build a Database"** → เลือก **Free (M0)**
3. เลือก Region ใกล้บ้าน เช่น Singapore → กด **Create**

**2.2 สร้าง Database User:**
1. ไปที่ **Database Access** (เมนูซ้าย) → กด **Add New Database User**
2. ตั้ง Username และ Password (จดไว้ด้วย)
3. เลือก Role: **"Read and Write to any database"** → กด **Add User**

**2.3 อนุญาต IP ทุกคน (สำคัญมาก):**
1. ไปที่ **Network Access** (เมนูซ้าย) → กด **Add IP Address**
2. กด **"Allow Access from Anywhere"** → จะได้ `0.0.0.0/0`
3. กด **Confirm**

> 💡 ถ้าไม่ทำขั้นตอนนี้จะ connect ไม่ได้จากเครื่องอื่น

**2.4 คัดลอก Connection String:**
1. ไปที่ **Database** → กด **Connect** → เลือก **"Drivers"**
2. เลือก Driver: **Python** → คัดลอก connection string
3. จะได้รูปแบบ:
```
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
```
4. แทนที่ `<username>` และ `<password>` ด้วยที่ตั้งไว้ในขั้นที่ 2.2

---

### ขั้นตอนที่ 3 — ตั้งค่า Backend

```bash
cd Backend/botgold
```

**สร้าง virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**ติดตั้ง packages:**
```bash
pip install -r requirements.txt
pip install certifi bcrypt==4.0.1
pip install pandas beautifulsoup4 requests kaggle
```

**สร้างไฟล์ `.env`** ใน `Backend/botgold/`:
```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
DB_NAME=goldbot_db
JWT_SECRET=ใส่ค่าสุ่มอะไรก็ได้ยาว ๆ
JWT_EXPIRE_HOURS=24
OLLAMA_HOST=http://localhost:11434
CHROMA_PATH=./chroma_db
CHROMA_COLLECTION=gold_knowledge
FRONTEND_URL=http://localhost:3000
```

---

### ขั้นตอนที่ 4 — โหลด Ollama Models

```bash
# Model สำหรับ Embedding (จำเป็น)
ollama pull nomic-embed-text

# Model สำหรับตอบคำถาม (เลือกอันใดอันหนึ่ง)
ollama pull llama3.2       # เร็ว ขนาด ~2GB แนะนำ
ollama pull gpt-oss:20b    # แม่นกว่า แต่ช้ากว่า ขนาด ~13GB
```

---

### ขั้นตอนที่ 5 — เตรียมข้อมูลและ Embed

> ⚠️ ไฟล์ `chroma_db/` ไม่ได้อยู่ใน repo ต้องทำขั้นตอนนี้ทุกคน

**5.1 ตั้งค่า Kaggle API:**
- ไปที่ https://kaggle.com → Account → API → **Create New Token**
- จะได้ไฟล์ `kaggle.json` ให้วางไว้ที่:
  - Windows: `C:\Users\<username>\.kaggle\kaggle.json`
  - Mac/Linux: `~/.kaggle/kaggle.json`

**5.2 สร้าง `__init__.py` ใน folders (สำคัญ):**
```bash
# Windows
type nul > cleaners\__init__.py
type nul > converters\__init__.py
type nul > embedder\__init__.py

# Mac/Linux
touch cleaners/__init__.py converters/__init__.py embedder/__init__.py
```

**5.3 โหลด Clean Scrape และ Clean ข้อมูลทั้งหมด:**
```bash
python main.py
```

> `main.py` จะทำครบทุกขั้นตอนอัตโนมัติ ได้แก่ download จาก Kaggle, clean datasets, scrape Wikipedia และ clean Wikipedia text

**5.4 Embed ข้อมูลลง ChromaDB:**
```bash
# ต้องเปิด Ollama ค้างไว้ก่อน (ใช้เวลานานประมาณ 10-30 นาที)
python embedder/embed.py

# ถ้าต้องการ embed ใหม่ทั้งหมด (ลบของเก่าก่อน)
python embedder/embed.py --force
```

---

### ขั้นตอนที่ 6 — รัน Backend

```bash
# อยู่ใน Backend/botgold และ activate venv แล้ว
python -m uvicorn app:app --reload --port 8000
```

ถ้าขึ้น `✅ MongoDB connected: goldbot_db` แสดงว่าพร้อมใช้งาน

ทดสอบ API ได้ที่: http://localhost:8000/docs

---

### ขั้นตอนที่ 7 — ตั้งค่า Frontend

```bash
cd Frontend/goldbot
```

**สร้างไฟล์ `.env`** ใน `Frontend/goldbot/`:
```env
REACT_APP_API_URL=http://localhost:8000
```

**ติดตั้ง packages:**
```bash
npm install
```

**รัน Frontend:**
```bash
npm start
```

เบราว์เซอร์จะเปิดที่ http://localhost:3000 อัตโนมัติ

---

## 🖥️ วิธีรันทุกครั้งที่เปิดเครื่อง

เปิด **3 terminal** แยกกัน:

**Terminal 1 — Ollama:**
```bash
ollama serve
```

**Terminal 2 — Backend:**
```bash
cd Backend/botgold
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
python -m uvicorn app:app --reload --port 8000
```

**Terminal 3 — Frontend:**
```bash
cd Frontend/goldbot
npm start
```

---

## 🔑 API Endpoints

| Method | Endpoint | คำอธิบาย |
|--------|----------|---------|
| POST | `/auth/register` | สมัครสมาชิก |
| POST | `/auth/login` | เข้าสู่ระบบ |
| GET | `/chat/rooms` | ดูประวัติห้องแชท |
| POST | `/chat/rooms` | สร้างห้องแชทใหม่ |
| DELETE | `/chat/rooms/{id}` | ลบห้องแชท |
| GET | `/chat/rooms/{id}/messages` | ดูข้อความในห้อง |
| POST | `/chat/rooms/{id}/messages` | ส่งข้อความ |
| POST | `/chat/quick` | แชทเร็ว (สร้างห้องอัตโนมัติ) |

---

## ⚠️ ข้อควรระวัง

- ห้าม commit ไฟล์ `.env`, `chroma_db/`, `data/`, `kaggle.json` ขึ้น Git เด็ดขาด
- Chatbot นี้ให้ข้อมูลเพื่อการศึกษาเท่านั้น ไม่แนะนำให้ซื้อ/ขายทองโดยตรง
- ไม่ทำนายราคาทองในอนาคต

---

## 🐛 ปัญหาที่พบบ่อย

| ปัญหา | วิธีแก้ |
|-------|--------|
| `npm` not found | ติดตั้ง Node.js จาก nodejs.org แล้วเปิด terminal ใหม่ |
| `uvicorn` not found | รัน `python -m uvicorn ...` แทน |
| CORS error | ตรวจสอบ `allow_origins` ใน `app.py` |
| MongoDB SSL error | รัน `pip install certifi` และตรวจสอบ `database.py` |
| `nomic-embed-text` not found | รัน `ollama pull nomic-embed-text` |
| bcrypt error | รัน `pip install bcrypt==4.0.1` |
| PowerShell ไม่ให้รัน script | เปิด CMD แทน PowerShell หรือรัน `Set-ExecutionPolicy RemoteSigned` |
| MongoDB Network Access error | ไปที่ Atlas → Network Access → Allow Access from Anywhere |
| `No module named 'cleaners'` | รัน `type nul > cleaners\__init__.py` (Windows) |
| `No module named 'pandas'` | รัน `pip install pandas beautifulsoup4 requests` |
| embed.py ติด ConnectTimeout | ตรวจสอบ Ollama เปิดอยู่ด้วย `ollama list` และแก้ host เป็น `http://localhost:11434` ใน embed.py |
| Ollama port ถูกใช้งานอยู่แล้ว | Ollama เปิดอยู่แล้ว ไม่ต้องรัน `ollama serve` อีก รัน backend ได้เลย |
