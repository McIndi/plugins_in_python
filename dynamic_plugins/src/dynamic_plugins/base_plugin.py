"""Base class for plugins loaded by the dynamic file scanner."""

from __future__ import annotations


class BasePlugin:
    """Inherit from this class inside a ``.python`` plugin file.

    Subclasses must define a unique :attr:`name` string and implement
    :meth:`run`.

    Example (``hello.python``)::

        from dynamic_plugins import BasePlugin

        class HelloPlugin(BasePlugin):
            name = "hello"

            def run(self) -> str:
                return "Hello, world!"
    """

    #: Unique identifier for this plugin.  Must be overridden.
    name: str = ""

    def run(self) -> str:
        """Execute the plugin.  Override in subclasses."""
        raise NotImplementedError(f"{type(self).__name__} must implement run()")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r})"
