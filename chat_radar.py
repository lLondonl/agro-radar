import asyncio
import os
import re

import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Сессия рядом с этим файлом — та же, что у chat_parser.py и dialogs.py
BASE = os.path.dirname(os.path.abspath(__file__))
SESSION = os.path.join(BASE, "radar")

load_dotenv(os.path.join(BASE, ".env"))
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

CHATS = ["grainrussian", "rf_zerno", "zerno_rossiya", "zernofond", -5463887823]  # последний — «Тест радара»
SELL_WORDS = ["продам", "продаю", "реализуем", "в наличии"]
CROP_WORDS = ["пшениц", "ячмен", "подсолн", "кукуруз", "лён", "рапс"]
STOP_WORDS = ["куплю", "закупаем", "услуги"]
# Регионы — основы слов маленькими буквами. Пустой список [] — присылать все регионы
REGION_WORDS = ["краснод", "ростов", "ставроп", "москв", "кубан", "сарат"]

client = TelegramClient(SESSION, API_ID, API_HASH)

seen = set()


def fingerprint(text):
    return re.sub(r"\W+", "", text.lower())[:200]


def is_offer(text):
    low = text.lower()
    if any(w in low for w in STOP_WORDS):
        return False
    if REGION_WORDS and not any(w in low for w in REGION_WORDS):
        return False
    return any(w in low for w in SELL_WORDS) and any(w in low for w in CROP_WORDS)


def notify(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": ADMIN_ID, "text": text[:4000], "disable_web_page_preview": True},
            timeout=15,
        )
    except requests.RequestException as e:
        print("Не отправилось:", e)


@client.on(events.NewMessage(chats=CHATS))
async def on_message(event):
    text = event.raw_text or ""
    if not is_offer(text):
        return
    fp = fingerprint(text)
    if fp in seen:
        print("Дубль, пропускаю")
        return
    seen.add(fp)
    chat = await event.get_chat()
    link = f"https://t.me/{chat.username}/{event.id}" if getattr(chat, "username", None) else ""
    await asyncio.to_thread(notify, f"Предложение ({chat.title}):\n\n{text}\n\n{link}")
    print("Отправлено:", text[:60])


client.start()
print("Радар слушает чаты. Остановить: Ctrl+C")
client.run_until_disconnected()
