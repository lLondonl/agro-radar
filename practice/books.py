import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl.styles import Font

# Файлы Excel читаются и сохраняются рядом с этой программой (папка practice)
HERE = os.path.dirname(os.path.abspath(__file__))

RATING = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
rows = []

for page in range(1, 51):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    r = requests.get(url, timeout=15)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        price_text = card.select_one("p.price_color").get_text()
        rows.append({
            "Название": link["title"],
            "Цена, £": float(price_text.replace("£", "")),
            "Рейтинг": RATING.get(card.select_one("p.star-rating")["class"][1], 0),
            "В наличии": "In stock" in card.select_one("p.availability").get_text(),
            "Ссылка": "https://books.toscrape.com/catalogue/" + link["href"],
        })
    print(f"Страница {page}/50, товаров: {len(rows)}")
    time.sleep(0.3)

df = pd.DataFrame(rows)
df.to_excel(os.path.join(HERE, "books.xlsx"), index=False)
print("Сохранено в", os.path.join(HERE, "books.xlsx"))

wb = load_workbook(os.path.join(HERE, "books.xlsx"))
ws = wb.active
for cell in ws[1]:
    cell.font = Font(bold=True)
for col, width in zip("ABCDE", [50, 10, 10, 12, 60]):
    ws.column_dimensions[col].width = width
ws.freeze_panes = "A2"
ws.auto_filter.ref = ws.dimensions
wb.save(os.path.join(HERE, "books.xlsx"))
