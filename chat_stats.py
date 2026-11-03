import os

import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(BASE, "chats.xlsx"))

print(f"Всего объявлений о продаже: {len(df)}\n")
print("По чатам:")
print(df["Чат"].value_counts().to_string())
print("\nСамое старое и самое свежее по каждому чату:")
print(df.groupby("Чат")["Дата"].agg(["min", "max"]).to_string())

low = df["Текст"].str.lower()
crops = {"Пшеница": "пшениц", "Ячмень": "ячмен", "Подсолнечник": "подсолн",
         "Кукуруза": "кукуруз", "Лён": "лён|льна", "Рапс": "рапс", "Горох/нут": "горох|нут"}
print("\nПо культурам:")
for name, pattern in crops.items():
    print(f"{name:14} {low.str.contains(pattern).sum()}")
