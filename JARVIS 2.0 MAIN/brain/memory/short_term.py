class ShortTermMemory:

    def __init__(self):
        self.memory = []

    def add(self, item):
        self.memory.append(item)

    def all(self):
        return self.memory

    def clear(self):
        self.memory.clear()