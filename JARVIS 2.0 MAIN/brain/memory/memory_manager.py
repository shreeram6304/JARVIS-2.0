class MemoryManager:
    """
    Central memory controller for JARVIS.
    """

    def __init__(self, short_term, long_term, vector_memory):
        self.short_term = short_term
        self.long_term = long_term
        self.vector_memory = vector_memory

    def remember(self, item):
        self.short_term.add(item)

    def learn(self, item):
        self.long_term.add(item)

    def recall(self, query):
        return self.vector_memory.search(query)

    def context(self):
        return {
            "short_term": self.short_term.all(),
            "long_term": self.long_term.all()
        }

    def clear_short_term(self):
        self.short_term.clear()