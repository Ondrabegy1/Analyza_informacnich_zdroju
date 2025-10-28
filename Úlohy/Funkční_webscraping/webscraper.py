import requests
from bs4 import BeautifulSoup
import hashlib
import json
import os
from datetime import datetime
import time

# Nastavená cesta pro ukládání (jsem moc línej to měnit na relativní)
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

    content_block = soup.select_one("p.big") #Potřeba nahradit za celý článek, nikoliv perex
    full_content = extract_text(content_block)

    tags_block = soup.select(".tags a")
    tags = [t.get_text(strip=True) for t in tags_block] if tags_block else []

    if not date_str:
        date_str = datetime.now().isoformat()

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
