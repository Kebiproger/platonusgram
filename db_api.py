import sqlite3
from typing import Optional, Tuple

DB_PATH = "data.db"

def _get_conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    with _get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password_enc TEXT NOT NULL
            );
            """
        )
        conn.commit()

def save_user(telegram_id: int, username: str, password_enc: str) -> None:
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO users (telegram_id, username, password_enc)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                username=excluded.username,
                password_enc=excluded.password_enc;
            """,
            (telegram_id, username, password_enc),
        )
        conn.commit()

def get_user(telegram_id: int) -> Optional[Tuple[str, str]]:
    with _get_conn() as conn:
        cur = conn.execute(
            "SELECT username, password_enc FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = cur.fetchone()
        return row if row else None