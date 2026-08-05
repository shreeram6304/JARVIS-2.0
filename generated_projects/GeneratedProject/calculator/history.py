from typing import List, Dict, Any

class HistoryManager:
    """
    In-memory calculation history storage with maximum limit safety.
    """
    def __init__(self, max_items: int = 50):
        self.max_items = max_items
        self._history: List[Dict[str, Any]] = []

    def add_entry(self, expression: str, result: Any) -> Dict[str, Any]:
        """Appends a calculation record to history."""
        entry = {
            "id": len(self._history) + 1,
            "expression": expression,
            "result": str(result)
        }
        self._history.insert(0, entry) # Most recent first
        if len(self._history) > self.max_items:
            self._history.pop()
        return entry

    def get_all(self) -> List[Dict[str, Any]]:
        """Returns all history items."""
        return self._history

    def clear(self) -> None:
        """Clears calculation history."""
        self._history.clear()