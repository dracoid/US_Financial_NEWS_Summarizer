# app/db.py

import sqlite3
from .config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            title TEXT,
            published_dt TEXT,
            link TEXT UNIQUE,
            summary TEXT
        )
    """)
    conn.commit()
    conn.close()
