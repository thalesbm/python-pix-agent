# sessions/store.py
import sqlite3
from contextlib import closing
from typing import Optional, Tuple

class SessionStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        is_uri = str(self.db_path).startswith("file:")
        conn = sqlite3.connect(
            self.db_path, timeout=5.0, isolation_level=None,
            check_same_thread=False, uri=is_uri
        )
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=3000;")
        return conn

    def _init_db(self):
        with closing(self._connect()) as con:
            con.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
              thread_id   TEXT PRIMARY KEY,
              waiting     INTEGER NOT NULL DEFAULT 0,
              last_prompt TEXT,
              updated_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f','now'))
            );
            """)

    def set_waiting(self, thread_id: str, waiting: bool, last_prompt: Optional[str]=None):
        with closing(self._connect()) as con:
            con.execute("BEGIN IMMEDIATE;")
            con.execute("""
            INSERT INTO sessions(thread_id, waiting, last_prompt)
            VALUES (?, ?, ?)
            ON CONFLICT(thread_id) DO UPDATE SET
              waiting=excluded.waiting,
              last_prompt=excluded.last_prompt,
              updated_at=strftime('%Y-%m-%d %H:%M:%f','now');
            """, (thread_id, int(waiting), last_prompt))
            con.execute("COMMIT;")

    def get_waiting(self, thread_id: str) -> Tuple[bool, Optional[str]]:
        with closing(self._connect()) as con:
            row = con.execute(
                "SELECT waiting, last_prompt FROM sessions WHERE thread_id=?",
                (thread_id,)
            ).fetchone()
            if not row:
                return False, None
            return bool(row[0]), row[1]
