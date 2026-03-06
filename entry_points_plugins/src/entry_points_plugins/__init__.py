"""Entry-points based plugin system."""

from .base_plugin import BasePlugin
from .loader import PluginLoader

__all__ = ["BasePlugin", "PluginLoader"]
