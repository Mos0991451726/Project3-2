import os
import re

SCRAPED_PATH = "./scraped"
CLEANED_PATH = "./scraped/cleaned"

def clean_text(text: str) -> str:
    # ลบ citation เช่น [1], [23], [note 1], [a]
    text = re.sub(r'\[\w[\w\s]*\]', '', text)

    # ลบ reference section ท้ายไฟล์ (== References == เป็นต้น)
    text = re.sub(r'\n==[^=].*', '', text)

    # ลบบรรทัดที่มีแต่ตัวเลข หรือ สัญลักษณ์พิเศษ
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # ข้ามบรรทัดว่างซ้อนกัน
        if not line:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            continue
        # ข้ามบรรทัดสั้นมาก (น้อยกว่า 30 ตัวอักษร) เช่น หัวข้อย่อย
        if len(line) < 30:
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()

def clean_wiki():
    os.makedirs(CLEANED_PATH, exist_ok=True)

    cleaned_files = []
    for filename in os.listdir(SCRAPED_PATH):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(SCRAPED_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        cleaned = clean_text(raw)

        out_path = os.path.join(CLEANED_PATH, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        original_lines = len(raw.splitlines())
        cleaned_lines  = len(cleaned.splitlines())
        print(f"{filename}: {original_lines} → {cleaned_lines} lines (ตัดออก {original_lines - cleaned_lines} lines)")
        cleaned_files.append(out_path)

    print(f"\nWiki cleaned! {len(cleaned_files)} files → {CLEANED_PATH}")
    return cleaned_files

if __name__ == "__main__":
    clean_wiki()
