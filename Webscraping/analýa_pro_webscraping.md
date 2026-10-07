### 1. Prozkoumejte soubor robots.txt (je k dispozici?, co v něm je, je tam schéma stránky - jak vypadá, časové omezení, jiná omezení).

```
# CN robots.txt
User-agent: *
Disallow: /.*
Disallow: /vyhledavani/
Disallow: /tema/

User-agent: CCBot
Disallow: /

# For new training only
User-agent: GPTBot
Disallow: /
User-agent: ChatGPT-User
Disallow: /   # Marker for disabling Bard and Vertex AI
User-agent: Google-Extended
Disallow: /   # Speech synthesis
User-agent: FacebookBot
Disallow: /   # Multi-purpose, commercial uses; including LLMs
User-agent: Omgilibot
Disallow: /   #suggested by SPIR
User-agent: MachineLearning
Disallow: /

Sitemap: https://www.ceskenoviny.cz/sitemap.php
Sitemap: https://www.ceskenoviny.cz/sitemap_zpravy.php
Sitemap: https://www.ceskenoviny.cz/sitemap_zpravy_pr.php
```

Robots.txt je přítomný a dle kódu je v něm možné zjistit několik restrikcí. Kód jasně zakazuje přístup k /vyhledavani/ a /tema/, dále jsou zde vyjímky pro user-agenty (např. GPTBot,ChatGPT-User apod.), pro které je opět kompletní zákaz. Na konci kódu jsou uvedeny sitemapy pro celý web, zprávy a tiskové zprávy. V kódu se nenachází žádný způsob časového omezení.

---

### 2. Prozkoumejte strukturu sídla - hlavní nadpis, perex (úvodní odstavec), autor článku, hlavní obrázek článku, odkazy na články, ostatní důležité články, diskuse k článku. Vytvořte základní hierarchickou strukturu stránky významných částí stránky.

#### Článek (root container)

#### Hlava (header článku)
- název článku (H1)  
- meta informace (autor, datum, případně “Aktualizováno”)  
- perex / úvodní odstavec / shrnutí  
- hlavní obrázek + popisek obrázku  

#### Tělo článku (obsah)
- nadpisy (H2, H3 apod.)  
- odstavce, citace, bloky (např. „Image: …“, „Autor: …“)  
- případně vložené vizuální nebo mediální prvky  
- odkazy v textu na jiné články či externí zdroje  

#### „Čtěte také“ / související články (sekce)
- seznam odkazů na jiné články  

#### Diskuse a komentáře pod článkem (pokud je povolena)
- formulář pro přidání komentáře  
- seznam komentářů  

#### Pata (footer)
- odkazy: O nás, Kontakt, Podmínky užití, RSS, sociální sítě  
- copyright / ISSN  
- další navigační odkazy a reklamy  

---

### 3. Připravte si pro výše uvedené oblasti selektory s využitím konzole prohlížeče.

| Část stránky | Příklad CSS selektoru / zápis v konzoli |
|--------------|--------------------------------------------|
| Název článku (H1) | `document.querySelector(".box-article > h1:nth-child(1)")` |
| Meta údaje (autor, datum) | `document.querySelector(".info")` |
| Perex / úvodní odstavec | `document.querySelector("#branding")` |
| Hlavní obrázek článku | `document.querySelector(".box-img > span:nth-child(1) > img:nth-child(1)") ` |
| Popisek obrázku | `document.querySelector("span.grey:nth-child(1) > span:nth-child(1)")` |
| Obsah článku (tělo) | `document.querySelector(".content")` |
| Odkazy v textu | `document.querySelectorAll("p.big > a:nth-child(1)")` |
| Sekce „Čtěte také“ / související články | `document.querySelector(".dalsi-zpravy")` |
| Jednotlivý prvek v „Čtěte také“ | `document.querySelector("li.link:nth-child(n) > a:nth-child(1)")` kde n ∈ ℕ |
| Značky (tagy) | `document.querySelector(".tags")` |
| Komentáře / diskuse | `document.querySelector(".comments")` |
| Patička (footer) | `document.querySelector("#footer")` |
| Navigační menu | `document.querySelector("#menu-other")` nebo `document.querySelector("#header")` |
