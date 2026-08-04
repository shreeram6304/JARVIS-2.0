from .plan import Plan
from .task import Task


class Planner:
    """
    Creates an execution plan from a user's goal.
    """

    def __init__(self):
        self.plan = None

    def create_plan(self, goal: str):
        """
        Generate a fresh execution plan.
        """

        self.plan = Plan(goal)

        goal_lower = goal.lower()

        if "website" in goal_lower or "web" in goal_lower:

            steps = [
                ("Analyze user requirements", "coding"),
                ("Design project architecture", "coding"),
                ("Create project structure", "coding"),
                ("Generate backend", "coding"),
                ("Generate frontend", "coding"),
                ("Generate configuration files", "coding"),
                ("Build project", "coding"),
                ("Test project", "coding"),
                ("Fix project issues", "coding"),
                ("Deliver final project", "coding"),
            ]

        else:

            steps = [
                ("Analyze request", "coding"),
                ("Design solution", "coding"),
                ("Execute task", "coding"),
                ("Verify result", "coding"),
                ("Deliver result", "coding"),
            ]

        for description, agent in steps:

            task = Task(
                name=description,
                agent=agent
            )

            # Give every task access to the complete plan
            task.plan = self.plan

            self.plan.add(task)

        return self.plan