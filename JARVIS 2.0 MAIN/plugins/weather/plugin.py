from plugins.core.plugin import Plugin


class WeatherPlugin(Plugin):

    @property
    def name(self):
        return "Weather"

    def initialize(self, kernel):
        print("Weather Plugin Initialized")

    def shutdown(self):
        print("Weather Plugin Shutdown")