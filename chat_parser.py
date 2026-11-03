import asyncio
import os

import pandas as pd
from dotenv import load_dotenv
from telethon import TelegramClient

# Сессия и Excel всегда лежат рядом с этим файлом, откуда бы ни запускали
BASE = os.path.dirname(os.path.abspath(__file__))
SESSION = os.path.join(BASE, "radar")
OUT_FILE = os.path.join(BASE, "chats.xlsx")

load_dotenv(os.path.join(BASE, ".env"))
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# @имена групп без @ или числовые ID частных групп (без кавычек)
CHATS = ["grainrussian", "rf_zerno", "zerno_rossiya", "zernofond", -5463887823]  # последний — «Тест радара»
SELL_WORDS = ["продам", "продаю", "продаем", "продаём", "реализ", "в продаже", "в наличии"]
CROP_WORDS = ["пшениц", "ячмен", "подсолн", "кукуруз", "лён", "льна", "рапс", "горох", "нут"]
STOP_WORDS = ["куплю", "купим", "закупаем", "закупка", "покупаем", "примем", "принимаем", "услуги"]


def match(text):
    low = text.lower()
    if any(w in low for w in STOP_WORDS):
        return False
    return any(w in low for w in SELL_WORDS) and any(w in low for w in CROP_WORDS)


async def main():
    rows = []
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        for chat in CHATS:
            entity = await client.get_entity(chat)
            title = getattr(entity, "title", str(chat))
            username = getattr(entity, "username", None)
            async for msg in client.iter_messages(entity, limit=200):
                if msg.text and match(msg.text):
                    rows.append({
                        "Дата": msg.date.astimezone().strftime("%Y-%m-%d %H:%M"),
                        "Чат": title,
                        "Текст": msg.text.replace("\n", " "),
                        "Ссылка": f"https://t.me/{username}/{msg.id}" if username else "",
                    })
            print(f"{title}: готово, всего найдено {len(rows)}")
            await asyncio.sleep(2)   # пауза, чтобы Telegram не ограничил аккаунт
    pd.DataFrame(rows).to_excel(OUT_FILE, index=False)
    print("Сохранено в", OUT_FILE)


asyncio.run(main())
