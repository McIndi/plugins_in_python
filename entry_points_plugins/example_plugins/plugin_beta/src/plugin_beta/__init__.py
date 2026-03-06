"""Plugin Beta — an example entry-point plugin."""

from entry_points_plugins import BasePlugin


class BetaPlugin(BasePlugin):
    """The second example plugin."""

    name = "beta"

    def run(self) -> str:
        return "Greetings from Beta plugin!"
