"""Base class for entry-point plugins."""

from __future__ import annotations


class BasePlugin:
    """Inherit from this class to create an entry-point plugin.

    Subclasses must define a unique :attr:`name` string and implement
    :meth:`run`.

    Example::

        from entry_points_plugins import BasePlugin

        class MyPlugin(BasePlugin):
            name = "my_plugin"

            def run(self) -> str:
                return "Hello from MyPlugin!"
    """

    #: Unique identifier for this plugin.  Must be overridden.
    name: str = ""

    def run(self) -> str:
        """Execute the plugin.  Override in subclasses."""
        raise NotImplementedError(f"{type(self).__name__} must implement run()")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r})"
