from agents.base_agent import BaseAgent


class PlanningAgent(BaseAgent):

    @property
    def name(self):
        return "planner"

    def execute(self, task):
        print(f"[PlanningAgent] {task}")
        return task