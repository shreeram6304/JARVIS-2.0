from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    Base class for every JARVIS plugin.
    """

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def initialize(self, kernel):
        pass

    @abstractmethod
    def shutdown(self):
        pass