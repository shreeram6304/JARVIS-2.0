from agents.base_agent import BaseAgent
from agents.developer_brain import DeveloperBrain
from builder.pipeline import DevelopmentPipeline


class CodingAgent(BaseAgent):

    @property
    def name(self):
        return "coding"

    @property
    def description(self):
        return "Autonomous software development agent."

    def __init__(self):

        self.developer = DeveloperBrain()
        self.pipeline = DevelopmentPipeline()

    def execute(self, task, goal):

        print(f"\n[CodingAgent]")
        print(f"Task : {task.name}")
        print(f"Goal : {goal}")

        project = self.developer.generate_project(
            goal,
            task.plan
        )

        report = self.pipeline.execute(
            "GeneratedProject",
            project
        )

        return report