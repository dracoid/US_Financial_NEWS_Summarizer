# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# 환경 변수에서 설정값 불러오기
EXCEL_PATH = os.getenv("EXCEL_FILE", "/app/history.xlsx")
DB_PATH = os.getenv("DB_FILE", "/app/news_summary.db")
DOCX_SAVE_DIR = os.getenv("OUTPUT_DIR", "/app/summary")

# 요약 저장 폴더 생성
os.makedirs(DOCX_SAVE_DIR, exist_ok=True)
