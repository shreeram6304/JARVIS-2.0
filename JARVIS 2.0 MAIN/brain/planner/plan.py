class Plan:
    """
    Collection of executable tasks.
    """

    def __init__(self, goal=""):
        self.goal = goal
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)

    def pending(self):
        return [t for t in self.tasks if t.status == "pending"]

    def completed(self):
        return [t for t in self.tasks if t.status == "completed"]