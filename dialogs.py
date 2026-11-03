import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient

BASE = os.path.dirname(os.path.abspath(__file__))
SESSION = os.path.join(BASE, "radar")

load_dotenv(os.path.join(BASE, ".env"))
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


async def main():
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        async for d in client.iter_dialogs():
            username = getattr(d.entity, "username", None)
            kind = "группа" if d.is_group else "канал" if d.is_channel else "личный"
            print(f"{d.id:>16}  {kind:7}  {d.name}  {'@' + username if username else ''}")


asyncio.run(main())
