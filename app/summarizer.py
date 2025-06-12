import time
import pandas as pd
from newspaper import Article, Config
from transformers import pipeline
from .config import EXCEL_PATH
from .db import get_connection

# HuggingFace 요약 모델
summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")

# User-Agent 설정 (403 차단 회피)
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
newspaper_config = Config()
newspaper_config.browser_user_agent = user_agent
newspaper_config.request_timeout = 10

def summarize_and_store():
    df = pd.read_excel(EXCEL_PATH)
    conn = get_connection()
    cursor = conn.cursor()

    # 먼저 이미 저장된 링크 목록 불러오기 → set으로 빠른 조회
    cursor.execute("SELECT link FROM news_summaries")
    processed_links = set(row[0] for row in cursor.fetchall())

    tickers = df['ticker'].unique()

    for ticker in tickers:
        df_t = df[df['ticker'] == ticker].sort_values(by='published_dt')

        for _, row in df_t.iterrows():
            link = row['link']
            title = row['title']
            date = row['published_dt']

            # ✅ 이미 저장된 기사 스킵
            if link in processed_links:
                print(f"[SKIP] 이미 저장됨: {title}")
                continue

            try:
                # 기사 크롤링
                article = Article(link, config=newspaper_config)
                article.download()
                article.parse()
                text = article.text.strip()

                if len(text) < 200:
                    raise ValueError("본문이 너무 짧음")

                # 요약
                input_text = text[:1024]
                max_len = min(130, len(input_text) // 2)

                summary = summarizer_model(
                    input_text,
                    max_length=max_len,
                    min_length=30,
                    do_sample=False
                )[0]['summary_text']

            except Exception as e:
                print(f"[Error] {link}: {e}")
                summary = "크롤링 금지로 요약 불가"

            # 저장 (성공/실패 불문)
            cursor.execute("""
                INSERT INTO news_summaries (ticker, title, published_dt, link, summary)
                VALUES (?, ?, ?, ?, ?)
            """, (ticker, title, date, link, summary))
            conn.commit()
            processed_links.add(link)  # 즉시 추가하여 중복 방지

            print(f"[✓] {ticker}: {title}")
            time.sleep(1)

    conn.close()
