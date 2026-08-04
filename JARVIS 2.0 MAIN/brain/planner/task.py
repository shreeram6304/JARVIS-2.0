class Task:
    """
    Represents a single executable task.
    """

    def __init__(self, name, agent, priority=1):
        self.name = name
        self.agent = agent
        self.priority = priority
        self.status = "pending"

    def start(self):
        self.status = "running"

    def finish(self):
        self.status = "completed"

    def fail(self):
        self.status = "failed"

    def __repr__(self):
        return f"<Task {self.name} | {self.agent} | {self.status}>"