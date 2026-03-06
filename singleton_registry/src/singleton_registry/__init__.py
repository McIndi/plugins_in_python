"""Singleton-registry plugin system."""

from .base_plugin import BasePlugin
from .registry import PluginRegistry

__all__ = ["BasePlugin", "PluginRegistry"]
