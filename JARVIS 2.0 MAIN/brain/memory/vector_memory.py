class VectorMemory:

    def __init__(self):
        self.data = []

    def add(self, text):
        self.data.append(text)

    def search(self, query):
        results = []

        for item in self.data:
            if query.lower() in item.lower():
                results.append(item)

        return results