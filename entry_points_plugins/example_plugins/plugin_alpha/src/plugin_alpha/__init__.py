"""Plugin Alpha — an example entry-point plugin."""

from entry_points_plugins import BasePlugin


class AlphaPlugin(BasePlugin):
    """The first example plugin."""

    name = "alpha"

    def run(self) -> str:
        return "Hello from Alpha plugin!"
