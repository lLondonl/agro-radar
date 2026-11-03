import asyncio
import csv
import os
import re
from datetime import datetime

import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events

from radar_config import CHATS, CROP_WORDS, LOG_FILE, REGION_WORDS, SELL_WORDS, STOP_WORDS

BASE = os.path.dirname(os.path.abspath(__file__))
SESSION = os.path.join(BASE, "radar")

load_dotenv(os.path.join(BASE, ".env"))
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

client = TelegramClient(SESSION, API_ID, API_HASH)
seen = set()


def is_offer(text):
    low = text.lower()
    if any(w in low for w in STOP_WORDS):
        return False
    if REGION_WORDS and not any(w in low for w in REGION_WORDS):
        return False
    return any(w in low for w in SELL_WORDS) and any(w in low for w in CROP_WORDS)


def fingerprint(text):
    return re.sub(r"\W+", "", text.lower())[:200]


def notify(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": ADMIN_ID, "text": text[:4000], "disable_web_page_preview": True},
            timeout=15,
        )
    except requests.RequestException as e:
        print("Не отправилось:", e)


LOG_PATH = os.path.join(BASE, LOG_FILE)


def create_log():
    # Создаём журнал с заголовками сразу при запуске, чтобы файл был виден
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", newline="", encoding="utf-8-sig") as f:
            csv.writer(f, delimiter=";").writerow(["Найдено", "Чат", "Дата поста", "Текст", "Ссылка"])


def log(chat_title, date, text, link):
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), chat_title, date,
                    text.replace("\n", " "), link])


@client.on(events.NewMessage(chats=CHATS))
async def on_message(event):
    text = event.raw_text or ""
    if not is_offer(text):
        return
    fp = fingerprint(text)
    if fp in seen:
        return
    seen.add(fp)
    chat = await event.get_chat()
    title = getattr(chat, "title", "") or str(event.chat_id)
    link = f"https://t.me/{chat.username}/{event.id}" if getattr(chat, "username", None) else ""
    date = event.date.astimezone().strftime("%Y-%m-%d %H:%M")
    log(title, date, text, link)
    await asyncio.to_thread(notify, f"Предложение ({title}):\n\n{text}\n\n{link}")
    print(datetime.now().strftime("%H:%M"), "→", title, text[:60].replace("\n", " "))


create_log()
client.start()
print(f"Журнал: {LOG_PATH}")
print(f"Агро-радар слушает {len(CHATS)} чатов. Остановить: Ctrl+C")
client.run_until_disconnected()
