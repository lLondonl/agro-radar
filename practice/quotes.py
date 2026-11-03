import time

import requests
from bs4 import BeautifulSoup

BASE = "https://quotes.toscrape.com"
url = BASE + "/"
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

print("Готово, всего цитат:", len(rows))

counts = {}
for row in rows:
    counts[row["author"]] = counts.get(row["author"], 0) + 1

top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
for author, n in top:
    print(f"{author}: {n}")