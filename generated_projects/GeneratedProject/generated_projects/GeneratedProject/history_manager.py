import uuid
from datetime import datetime
import threading
from typing import List, Dict, Any

class HistoryManager:
    """Thread-safe state manager for storing dynamic calculation history log."""

    def __init__(self, max_entries: int = 50):
        self.max_entries = max_entries
        self._history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def add_entry(self, expression: str, result: str) -> Dict[str, Any]:
        """Appends a new calculation result to history."""
        entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "expression": expression,
            "result": result
        }
        with self._lock:
            self._history.insert(0, entry)
            if len(self._history) > self.max_entries:
                self._history.pop()
        return entry

    def get_history(() -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._history)

    def clear(self) -> None:
        """Clears all history entries."""
        with self._lock:
            self._history.clear()