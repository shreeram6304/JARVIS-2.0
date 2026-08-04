class ServiceContainer:
    """
    Central registry for shared services.
    """

    def __init__(self):
        self._services = {}

    def register(self, name: str, service):
        self._services[name] = service

    def get(self, name: str):
        return self._services.get(name)

    def exists(self, name: str):
        return name in self._services

    def remove(self, name: str):
        self._services.pop(name, None)

    def clear(self):
        self._services.clear()