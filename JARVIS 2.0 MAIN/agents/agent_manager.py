class AgentManager:

    def __init__(self):
        self._agents = {}

    def register(self, agent):
        self._agents[agent.name] = agent

    def get(self, name):
        return self._agents.get(name)

    def execute(self, name, task, goal):

        agent = self.get(name)

        if not agent:
            raise ValueError(f"Agent '{name}' not found.")

        return agent.execute(task, goal)