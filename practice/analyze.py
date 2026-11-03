import os

import pandas as pd

# Файлы Excel читаются и сохраняются рядом с этой программой (папка practice)
HERE = os.path.dirname(os.path.abspath(__file__))

df = pd.read_excel(os.path.join(HERE, "books.xlsx"))

print("Всего книг:", len(df))
print("Средняя цена:", round(df["Цена, £"].mean(), 2))
print("\nСредняя цена по рейтингу:")
print(df.groupby("Рейтинг")["Цена, £"].mean().round(2))

print("\nТоп-5 дорогих с рейтингом 5:")
best = df[df["Рейтинг"] == 5].sort_values("Цена, £", ascending=False).head(5)
print(best[["Название", "Цена, £"]])

best.to_excel(os.path.join(HERE, "best_books.xlsx"), index=False)
