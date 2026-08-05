import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "calculator_history.db")

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL,
            result TEXT NOT NULL,
            calc_type TEXT NOT NULL DEFAULT 'standard',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_history(expression: str, result: str, calc_type: str = "standard") -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (expression, result, calc_type) VALUES (?, ?, ?)",
        (expression, str(result), calc_type)
    )
    conn.commit()
    item_id = cursor.lastrowid
    
    cursor.execute("SELECT id, expression, result, calc_type, created_at FROM history WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    return {
        "id": row["id"],
        "expression": row["expression"],
        "result": row["result"],
        "calc_type": row["calc_type"],
        "created_at": row["created_at"]
    }

def get_recent_history(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, expression, result, calc_type, created_at FROM history ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row["id"],
            "expression": row["expression"],
            "result": row["result"],
            "calc_type": row["calc_type"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]

def clear_all_history() -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    return True