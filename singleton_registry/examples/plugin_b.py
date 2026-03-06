"""Plugin B — example plugin demonstrating decorator-style registration."""

from singleton_registry import BasePlugin


@BasePlugin.register
class PluginB(BasePlugin):
    """A farewell plugin registered via the @BasePlugin.register decorator."""

    name = "plugin_b"

    def run(self) -> str:
        return "Goodbye from Plugin B!"
