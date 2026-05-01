import json
import sqlite3
from pathlib import Path
from typing import Any


class Storage:
    def __init__(self, db_path: str = "data/kernel_tool.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT NOT NULL,
                    source TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS domains (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT UNIQUE NOT NULL,
                    first_seen TEXT NOT NULL,
                    last_seen TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    handle TEXT UNIQUE NOT NULL,
                    first_seen TEXT NOT NULL,
                    last_seen TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_type TEXT NOT NULL,
                    entity TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def save_scan(self, target: str, source: str, result: dict[str, Any], created_at: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO scans(target, source, result_json, created_at) VALUES (?, ?, ?, ?)",
                (target, source, json.dumps(result), created_at),
            )

    def upsert_domain(self, domain: str, seen_at: str) -> bool:
        with self._connect() as conn:
            row = conn.execute("SELECT id FROM domains WHERE domain = ?", (domain,)).fetchone()
            if row:
                conn.execute("UPDATE domains SET last_seen = ? WHERE domain = ?", (seen_at, domain))
                return False
            conn.execute(
                "INSERT INTO domains(domain, first_seen, last_seen) VALUES (?, ?, ?)",
                (domain, seen_at, seen_at),
            )
            return True

    def upsert_profile(self, handle: str, seen_at: str) -> bool:
        with self._connect() as conn:
            row = conn.execute("SELECT id FROM profiles WHERE handle = ?", (handle,)).fetchone()
            if row:
                conn.execute("UPDATE profiles SET last_seen = ? WHERE handle = ?", (seen_at, handle))
                return False
            conn.execute(
                "INSERT INTO profiles(handle, first_seen, last_seen) VALUES (?, ?, ?)",
                (handle, seen_at, seen_at),
            )
            return True

    def save_alert(self, alert_type: str, entity: str, message: str, created_at: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO alerts(alert_type, entity, message, created_at) VALUES (?, ?, ?, ?)",
                (alert_type, entity, message, created_at),
            )

    def fetch_all(self, table: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(f"SELECT * FROM {table} ORDER BY id DESC").fetchall()
            return [dict(r) for r in rows]
