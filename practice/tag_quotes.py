import time

import requests
from bs4 import BeautifulSoup

BASE = "https://quotes.toscrape.com"

tag = input("Введите тег (например, love, humor, life): ").strip().lower()
url = f"{BASE}/tag/{tag}/"
rows = []

while url:
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    for q in soup.select("div.quote"):
        rows.append({
            "author": q.select_one("small.author").get_text(strip=True),
            "text": q.select_one("span.text").get_text(strip=True),
        })
    next_link = soup.select_one("li.next a")
    url = BASE + next_link["href"] if next_link else None
    print("Собрано:", len(rows))
    time.sleep(0.5)

if not rows:
    print(f"По тегу «{tag}» цитат не найдено")
else:
    print(f"\nТег «{tag}»: найдено {len(rows)} цитат\n")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row['author']}: {row['text'][:80]}")