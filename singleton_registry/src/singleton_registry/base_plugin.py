"""Base class for all plugins in the singleton-registry system."""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from .registry import PluginRegistry

if TYPE_CHECKING:
    pass


class BasePlugin:
    """Inherit from this class to create a plugin.

    Subclasses **must** define a unique :attr:`name` string attribute.

    Registration is done by calling the :meth:`register` classmethod, which
    writes the subclass into the singleton :class:`PluginRegistry`.  The
    classmethod also works as a zero-argument decorator::

        @BasePlugin.register
        class MyPlugin(BasePlugin):
            name = "my_plugin"
            ...

    Or call it explicitly after the class definition::

        class MyPlugin(BasePlugin):
            name = "my_plugin"
            ...

        MyPlugin.register()
    """

    #: Unique identifier used as the registry key.  Must be overridden.
    name: str = ""

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    @classmethod
    def register(cls, plugin_cls: Type["BasePlugin"] | None = None) -> Type["BasePlugin"]:
        """Register a plugin class with the singleton :class:`PluginRegistry`.

        Can be called in three ways:

        1. As a no-argument decorator: ``@BasePlugin.register``
        2. Directly on the subclass:   ``MyPlugin.register()``
        3. Explicitly with a class:    ``BasePlugin.register(MyPlugin)``
        """
        # When used as @BasePlugin.register (no parentheses), Python passes
        # the decorated class as the first positional argument.
        target = plugin_cls if plugin_cls is not None else cls

        if not target.name:
            raise ValueError(f"{target.__name__} must define a non-empty 'name' attribute")

        PluginRegistry().register(target.name, target)
        return target

    # ------------------------------------------------------------------
    # Plugin interface
    # ------------------------------------------------------------------

    def run(self) -> str:
        """Execute the plugin.  Override in subclasses."""
        raise NotImplementedError(f"{type(self).__name__} must implement run()")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r})"
