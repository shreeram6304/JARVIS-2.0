from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for every JARVIS agent.
    """

    @property
    @abstractmethod
    def name(self):
        """Unique agent name."""
        pass

    @property
    def description(self):
        """Human-readable description."""
        return "No description provided."

    @abstractmethod
    def execute(self, task, goal):
        """
        Execute the assigned task.

        Args:
            task: Task object assigned by the Planner.
            goal: Original user goal.

        Returns:
            Result of the execution.
        """
        pass