"""Plugin A — example plugin for the singleton-registry package."""

from singleton_registry import BasePlugin


class PluginA(BasePlugin):
    """A simple greeting plugin."""

    name = "plugin_a"

    def run(self) -> str:
        return "Hello from Plugin A!"


# Register with the singleton registry
PluginA.register()
