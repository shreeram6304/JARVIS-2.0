from pathlib import Path
import importlib


class PluginManager:

    def __init__(self):
        self.plugins = {}

    def register(self, plugin):
        self.plugins[plugin.name] = plugin

    def get(self, name):
        return self.plugins.get(name)

    def all(self):
        return self.plugins.values()

    def discover_plugins(self):
        """
        Automatically discover plugins inside the plugins folder.
        """

        plugins_dir = Path("plugins")

        if not plugins_dir.exists():
            return

        for folder in plugins_dir.iterdir():

            if not folder.is_dir():
                continue

            if folder.name == "core":
                continue

            try:
                module = importlib.import_module(
                    f"plugins.{folder.name}.plugin"
                )

                plugin = module.Plugin()

                self.register(plugin)

                print(f"[PluginManager] Loaded: {plugin.name}")

            except Exception as e:
                print(f"[PluginManager] Failed to load {folder.name}: {e}")