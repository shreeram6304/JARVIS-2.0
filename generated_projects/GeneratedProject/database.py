import sqlite3
import os
from typing import List, Dict, Any

DB_FILE = "calculator_history.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                mode TEXT NOT NULL DEFAULT 'standard',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_calculation(expression: str, result: str, mode: str = "standard") -> Dict[str, Any]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (expression, result, mode) VALUES (?, ?, ?)",
            (expression, str(result), mode)
        )
        conn.commit()
        calc_id = cursor.lastrowid
        cursor.execute("SELECT id, expression, result, mode, timestamp FROM history WHERE id = ?", (calc_id,))
        row = cursor.fetchone()
        return dict(row)

def get_history(limit: int = 50) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, expression, result, mode, timestamp FROM history ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def clear_history() -> bool:
    with get_db_connection() as conn:
        conn.execute("DELETE FROM history")
        conn.commit()
    return True