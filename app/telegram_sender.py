import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

from .config import DOCX_SAVE_DIR

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

async def send_all_docs_async():
    if not BOT_TOKEN or not CHAT_IDS:
        print("❌ BOT_TOKEN 또는 CHAT_IDS 설정 누락")
        return

    bot = Bot(token=BOT_TOKEN)

    files = [f for f in os.listdir(DOCX_SAVE_DIR) if f.endswith(".docx")]
    if not files:
        print("⚠️ 보낼 docx 파일이 없습니다.")
        return

    for file in files:
        file_path = os.path.join(DOCX_SAVE_DIR, file)

        for chat_id in CHAT_IDS:
            try:
                with open(file_path, "rb") as doc_file:
                    await bot.send_document(chat_id=chat_id.strip(), document=doc_file, filename=file)
                    print(f"📤 전송 완료: {file} → {chat_id.strip()}")
            except TelegramError as e:
                print(f"[Error] {file} 전송 실패: {e}")

def send_all_docs():
    asyncio.run(send_all_docs_async())
