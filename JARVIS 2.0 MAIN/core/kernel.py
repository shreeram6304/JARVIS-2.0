from core.service_container import ServiceContainer
from core.plugin_manager import PluginManager
from core.event_bus import EventBus
from brain.planner.planner import Planner
from agents.agent_manager import AgentManager



class Kernel:
    """
    JARVIS AI OS Kernel

    Responsible for initializing and managing
    the core infrastructure of JARVIS.
    """

    def __init__(self):
        self.container = ServiceContainer()
        self.plugins = PluginManager()
        self.events = EventBus()
        self.planner = Planner()
        self.agents = AgentManager()

    def initialize(self):
        print("[Kernel] Initializing...")

        self.container.register("event_bus", self.events)
        self.container.register("plugin_manager", self.plugins)

        print("[Kernel] Services registered.")

    def shutdown(self):
        print("[Kernel] Shutting down...")
        self.container.clear()