import sqlite3
import os

DB_NAME = "audit_log.db"


def init_db():
    """Initializes the SQLite database and creates the audit_logs table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            content_id TEXT PRIMARY KEY,
            creator_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            text_preview TEXT NOT NULL,
            groq_score REAL,
            stylometric_score REAL,
            combined_score REAL,
            assigned_label TEXT,
            lifecycle_status TEXT NOT NULL,
            creator_reasoning TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
