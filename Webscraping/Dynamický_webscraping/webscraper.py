from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import hashlib
import json
import os
import re
from datetime import datetime
import time

ROOT = "data"

def get_md5_hash(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest()[-8:]

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

date_pattern = re.compile(r'\b([0-3]?\d\.(?:[0-1]?\d)\.\d{4})\b(?!\s*,\s*\d{1,2}:\d{2})')
money_pattern = re.compile(r'\b(\d{1,3}(?:[ \u00A0]\d{3})*(?:,\d{2})?)\s*Kč\b')
temperature_pattern = re.compile(r'\b([+-]?\d+(?:,\d+)?)\s*°?\s*C\b', re.IGNORECASE)

def extract_text(tag):
    return tag.get_text(strip=True) if tag else None

def parse_article_soup(soup, url):
    title = extract_text(soup.select_one(".box-article > h1"))
    info = extract_text(soup.select_one(".info"))
    author = extract_text(soup.select_one(".author > a"))
    date_str = extract_text(soup.select_one("#published > span"))
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
    m_date = date_pattern.search(content)
    if m_date:
        tag = f"datum_nalezeno:{m_date.group(1)}"
        if tag not in tags:
            tags.append(tag)
    m_money = money_pattern.search(content)
    if m_money:
        tag = f"měna_nalezena:{m_money.group(1)} Kč"
        if tag not in tags:
            tags.append(tag)
    m_temp = temperature_pattern.search(content)
    if m_temp:
        tag = f"teplota_nalezena:{m_temp.group(1)} °C"
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
    folder = os.path.join(ROOT, domain, year, month)
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
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.ceskenoviny.cz/")
        page.wait_for_selector("a[href*='/zpravy/']")
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

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
        print("[DEBUG] Links:", links[:10])

        for url in links:
            try:
                page.goto(url)
                page.wait_for_selector("#articlebody", timeout=10000)
                html_art = page.content()
                soup_art = BeautifulSoup(html_art, "html.parser")
                art = parse_article_soup(soup_art, url)
                save_article(art)
                time.sleep(1)
            except Exception as e:
                print("[ERR]", url, e)
        browser.close()

if __name__ == "__main__":
    main()