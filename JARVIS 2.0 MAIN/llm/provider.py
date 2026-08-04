from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Base interface for every language model.
    """

    @abstractmethod
    def generate(self, prompt: str):
        """
        Generate a response from the model.
        """
        pass