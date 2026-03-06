"""Plugin loader: discovers plugins via importlib.metadata entry_points."""

from __future__ import annotations

from importlib.metadata import entry_points
from typing import Dict, Type

from .base_plugin import BasePlugin

#: The entry-point group this loader searches.
ENTRY_POINT_GROUP = "entry_points_plugins.plugins"


class PluginLoader:
    """Load plugins that have been registered via the ``entry_points_plugins.plugins``
    entry-point group.

    Any installed package can expose one or more plugins by adding entries to
    that group in its ``pyproject.toml``::

        [project.entry-points."entry_points_plugins.plugins"]
        my_plugin = "my_package:MyPluginClass"

    The loader calls :func:`importlib.metadata.entry_points` at runtime — no
    prior knowledge of the plugin packages is required.

    Example::

        loader = PluginLoader()
        plugins = loader.load()
        for name, cls in plugins.items():
            print(name, cls().run())

    Args:
        group: Entry-point group to query.  Defaults to
               ``"entry_points_plugins.plugins"``.
    """

    def __init__(self, group: str = ENTRY_POINT_GROUP) -> None:
        self.group = group

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self) -> Dict[str, Type[BasePlugin]]:
        """Return a ``{name: class}`` mapping of all installed plugins.

        Each entry point's *name* (the key in ``pyproject.toml``) becomes the
        dictionary key; the loaded class is the value.
        """
        plugins: Dict[str, Type[BasePlugin]] = {}

        for ep in entry_points(group=self.group):
            plugin_cls = ep.load()
            plugins[ep.name] = plugin_cls

        return plugins

    def __repr__(self) -> str:
        return f"PluginLoader(group={self.group!r})"
