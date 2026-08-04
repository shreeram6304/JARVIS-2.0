from brain.goal_parser import GoalParser
from brain.planner.planner import Planner
from agents.agent_manager import AgentManager
from agents.coding_agent import CodingAgent
from brain.executor import Executor


class JarvisBrain:
    """
    Central decision-making system for JARVIS.
    """

    def __init__(self):
        self.goal_parser = GoalParser()
        self.planner = Planner()
        self.agent_manager = AgentManager()
        self.executor = Executor(self.agent_manager)
        self.agent_manager.register(CodingAgent())

    def think(self, user_input: str):

        # Step 1: Understand the request
        goal = self.goal_parser.parse(user_input)

        print(f"[Brain] Intent: {goal.intent}")
        print(f"[Brain] Domain: {goal.domain}")
        print(f"[Brain] Framework: {goal.framework}")

        # Step 2: Create an execution plan
        plan = self.planner.create_plan(goal.target)

        result = None

        if goal.intent == "build":
            result = self.executor.execute(plan)

        return {
            "goal": goal,
            "plan": plan,
            "result": result
        }