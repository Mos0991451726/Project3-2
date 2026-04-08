import os
import requests
from bs4 import BeautifulSoup

OUTPUT_PATH = "./scraped"

URLS = [
    "https://en.wikipedia.org/wiki/Gold_as_an_investment",
    "https://en.wikipedia.org/wiki/Gold",
]

def scrape_wiki(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # ดึงเฉพาะเนื้อหาหลัก
    content = soup.find("div", {"id": "mw-content-text"})
    
    if content is None:
        print(f"Failed to get content from: {url}")
        return ""
    
    paragraphs = content.find_all("p")
    text = "\n".join([p.get_text() for p in paragraphs if p.get_text().strip()])
    
    return text

def scrape_all():
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    for url in URLS:
        # ใช้ชื่อ page เป็นชื่อไฟล์
        page_name = url.split("/wiki/")[-1]
        output_file = f"{OUTPUT_PATH}/{page_name}.txt"
        
        # เช็คว่ามีไฟล์แล้วไหม
        if os.path.exists(output_file):
            print(f"Already exists, skipping: {page_name}")
            continue
        
        print(f"Scraping: {url}")
        text = scrape_wiki(url)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"Saved: {page_name}.txt")

if __name__ == "__main__":
    scrape_all()