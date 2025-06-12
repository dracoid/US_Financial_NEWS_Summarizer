from app.db import init_db
from app.summarizer import summarize_and_store
from app.exporter import export_docx_all
from app.telegram_sender import send_all_docs  # ✅ 추가

def main():
    print("🛠 DB 초기화...")
    init_db()

    print("📰 뉴스 요약 시작...")
    summarize_and_store()

    print("📄 DOCX 변환 시작...")
    export_docx_all()

    print("📨 텔레그램 전송 시작...")
    send_all_docs()

    print("✅ 전체 작업 완료")

if __name__ == "__main__":
    main()
