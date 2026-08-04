import sqlite3
import os
from typing import List, Dict, Any

class HistoryManager:
    """Manages persistent calculation history stored in SQLite."""

    def __init__(self, db_path: str = "calculator_history.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Creates the history table if it does not exist."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expression TEXT NOT NULL,
                    result TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add_entry(self, expression: str, result: str) -> Dict[str, Any]:
        """Saves a calculation result to the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (expression, result) VALUES (?, ?)",
                (expression, str(result))
            )
            conn.commit()
            entry_id = cursor.lastrowid

            cursor.execute("SELECT id, expression, result, timestamp FROM history WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            return dict(row) if row else {"id": entry_id, "expression": expression, "result": str(result)}

    def get_recent(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Retrieves recent calculation entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, expression, result, timestamp FROM history ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def clear(self) -> bool:
        """Clears all entries from history."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM history")
            conn.commit()
            return True