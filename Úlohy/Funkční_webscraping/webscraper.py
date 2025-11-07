import requests
from bs4 import BeautifulSoup
import hashlib
import json
import os
import re
from datetime import datetime
import time

# Nastavená cesta pro ukládání (můžeš změnit na relativní)
ROOT = r"C:\Users\Ondra\Desktop\Škola\Analyza_informacnich_zdroju\Úlohy\Funkční_webscraping\JSON_výstupy"

def get_md5_hash(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest()[-8:]

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_text(tag):
    return tag.get_text(strip=True) if tag else None

def fetch_article_links():
    url = "https://www.ceskenoviny.cz/"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/"):
            full = "https://www.ceskenoviny.cz" + href
        else:
            full = href
        if "/zpravy/" in full:
            links.append(full)

    links = list(set(links))
    print("[DEBUG] Všechny vybrané odkazy:", links[:10])
    return links

# Regulární výrazy pro detekci a zachycení
date_pattern = re.compile(r'\b([0-3]?\d\.(?:[0-1]?\d)\.\d{4})\b(?!\s*,\s*\d{1,2}:\d{2})')
money_pattern = re.compile(r'\b(\d{1,3}(?:[ \u00A0]\d{3})*(?:,\d{2})?)\s*Kč\b')
temperature_pattern = re.compile(r'\b([+-]?\d+(?:,\d+)?)\s*°?\s*C\b', re.IGNORECASE)

def parse_article(url: str):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    title = extract_text(soup.select_one(".box-article > h1:nth-child(1)"))
    info = extract_text(soup.select_one(".info"))

    author = extract_text(soup.select_one(".author > a:nth-child(1)"))
    date_str = extract_text(soup.select_one("#published > span:nth-child(1)"))
    if info:
        parts = info.split(" - ")
        if len(parts) >= 2:
            author = parts[0].strip()
            date_str = parts[-1].strip()

    snippet = extract_text(soup.select_one("p.big"))

    content_block = soup.select_one("#articlebody")
    full_content = extract_text(content_block)

    tags_block = soup.select(".tags a")
    tags = [t.get_text(strip=True) for t in tags_block] if tags_block else []

    if not date_str:
        date_str = datetime.now().isoformat()

    content = full_content or ""

    # Datum
    m_date = date_pattern.search(content)
    if m_date:
        val = m_date.group(1)
        tag = f"datum_nalezeno:{val}"
        if tag not in tags:
            tags.append(tag)

    # Měna
    m_money = money_pattern.search(content)
    if m_money:
        val = m_money.group(1) + " Kč"
        tag = f"měna_nalezena:{val}"
        if tag not in tags:
            tags.append(tag)

    # Teplota
    m_temp = temperature_pattern.search(content)
    if m_temp:
        val = m_temp.group(1) + " °C"
        tag = f"teplota_nalezena:{val}"
        if tag not in tags:
            tags.append(tag)

    return {
        "title": title,
        "url": url,
        "date": date_str,
        "author": author,
        "source": "ceskenoviny.cz",
        "content_snippet": snippet,
        "full_content": full_content,
        "tags": tags
    }


def save_article(article: dict):
    dt = datetime.now()
    year = dt.strftime("%Y")
    month = dt.strftime("%m")

    domain = article["source"].split(".")[0]
    hashid = get_md5_hash(article["url"])

    folder = os.path.join(ROOT, "data", domain, year, month)
    ensure_dir(folder)

    filename = f"{domain}-{dt.strftime('%Y%m%d')}-{hashid}.json"
    path = os.path.join(folder, filename)

    if os.path.exists(path):
        print(f"[!] Duplikát, přeskočeno: {filename}")
        return

    with open(path, "w", encoding="utf-8") as f:
        json.dump(article, f, indent=4, ensure_ascii=False)

    print(f"[OK] Uloženo: {filename}")

def main():
    print("[*] Stahuji seznam článků...")
    links = fetch_article_links()
    print(f"[*] Nalezeno {len(links)} článků")

    for url in links:
        try:
            print(f" => {url}")
            art = parse_article(url)
            save_article(art)
            time.sleep(1)
        except Exception as e:
            print(f"[ERR] {e}")

if __name__ == "__main__":
    main()