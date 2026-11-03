import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Файлы Excel читаются и сохраняются рядом с этой программой (папка practice)
HERE = os.path.dirname(os.path.abspath(__file__))


def get_description(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print("  ошибка загрузки:", e)
        return ""
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    p = soup.select_one("#product_description + p")
    return p.get_text(strip=True) if p else ""


df = pd.read_excel(os.path.join(HERE, "books.xlsx"))
top = df.head(20).copy()

descriptions = []
for i, url in enumerate(top["Ссылка"], 1):
    descriptions.append(get_description(url))
    print(f"{i}/20 готово")
    time.sleep(0.5)

top["Описание"] = descriptions
top.to_excel(os.path.join(HERE, "books_top20.xlsx"), index=False)
print("Сохранено в", os.path.join(HERE, "books_top20.xlsx"))

