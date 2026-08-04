import sqlite3
import datetime
from typing import List, Dict, Any

class HistoryManager:
    """Handles storing and retrieving calculation history records using SQLite."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Create history table if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expression TEXT NOT NULL,
                    result TEXT NOT NULL,
                    calc_type TEXT DEFAULT 'standard',
                    timestamp TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_entry(self, expression: str, result: Any, calc_type: str = 'standard'):
        """Insert a calculation record."""
        now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO history (expression, result, calc_type, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (str(expression), str(result), calc_type, now_iso))
            conn.commit()

    def get_history(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Fetch recent history records ordered from newest to oldest."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, expression, result, calc_type, timestamp
                FROM history
                ORDER BY id DESC
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            return [
                {
                    'id': row['id'],
                    'expression': row['expression'],
                    'result': row['result'],
                    'calc_type': row['calc_type'],
                    'timestamp': row['timestamp']
                }
                for row in rows
            ]

    def clear_history(self):
        """Delete all history entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history')
            conn.commit()