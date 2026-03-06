"""Singleton plugin registry."""

from __future__ import annotations

from typing import Dict, Optional, Type


class PluginRegistry:
    """A singleton that maps plugin names to their classes.

    Because only one instance ever exists, every part of the application
    shares the same registry — no global variable needed.

    Example::

        registry = PluginRegistry()
        registry.register("my_plugin", MyPlugin)
        cls = registry.get("my_plugin")

    .. note::
        This implementation is not thread-safe.  If you need concurrent
        registration from multiple threads, protect :meth:`register` and
        :meth:`unregister` with a :class:`threading.Lock`.
    """

    _instance: Optional["PluginRegistry"] = None

    def __new__(cls) -> "PluginRegistry":
        if cls._instance is None:
            instance = super().__new__(cls)
            # Each attribute lives on the instance, not the class, so there
            # is no shared mutable class-level state to worry about.
            instance._plugins: Dict[str, Type] = {}
            cls._instance = instance
        return cls._instance

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def register(self, name: str, plugin_class: Type) -> None:
        """Add *plugin_class* to the registry under *name*."""
        self._plugins[name] = plugin_class

    def unregister(self, name: str) -> None:
        """Remove the plugin registered under *name* (if present)."""
        self._plugins.pop(name, None)

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get(self, name: str) -> Optional[Type]:
        """Return the plugin class for *name*, or ``None`` if not found."""
        return self._plugins.get(name)

    def all(self) -> Dict[str, Type]:
        """Return a shallow copy of the entire registry."""
        return dict(self._plugins)

    def __repr__(self) -> str:
        names = list(self._plugins.keys())
        return f"PluginRegistry(plugins={names})"
