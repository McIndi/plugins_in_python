"""Plugin loader: scans a directory for ``*.python`` plugin files."""

from __future__ import annotations

import inspect
import pathlib
import types
from typing import Dict, Type

from .base_plugin import BasePlugin


class PluginLoader:
    """Discover and load plugins from a directory.

    The loader scans *plugin_dir* for files that match ``*.python`` **and**
    do **not** start with an underscore.  Each matching file is imported as
    an isolated module; every top-level class that is a non-abstract subclass
    of :class:`BasePlugin` is collected.

    Example::

        loader = PluginLoader("plugins/")
        plugins = loader.load()
        # {"hello": HelloPlugin, "goodbye": GoodbyePlugin}

    Args:
        plugin_dir: Path to the directory that contains ``.python`` files.
    """

    def __init__(self, plugin_dir: str | pathlib.Path) -> None:
        self.plugin_dir = pathlib.Path(plugin_dir).resolve()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self) -> Dict[str, Type[BasePlugin]]:
        """Scan :attr:`plugin_dir` and return a ``{name: class}`` mapping.

        Only files whose names end with ``.python`` and do **not** begin with
        an underscore are considered.
        """
        plugins: Dict[str, Type[BasePlugin]] = {}

        for path in sorted(self.plugin_dir.glob("*.python")):
            if path.name.startswith("_"):
                continue  # skip private/helper files
            discovered = self._load_file(path)
            plugins.update(discovered)

        return plugins

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_file(self, path: pathlib.Path) -> Dict[str, Type[BasePlugin]]:
        """Read *path*, execute it as a Python module, and collect ``BasePlugin`` subclasses.

        We use :func:`compile` + :func:`exec` instead of
        ``importlib.util.spec_from_file_location`` because the standard
        machinery only recognises ``.py`` (and ``.pyc``) extensions, so
        it would return ``None`` for ``.python`` files.

        .. warning::
            ``exec`` runs the file's code in the current process with full
            privileges.  Only load plugins from **trusted sources**.  Never
            point the loader at a directory that untrusted users can write to.
        """
        module_name = f"_dynamic_plugin_{path.stem}"
        source = path.read_text(encoding="utf-8")
        code = compile(source, str(path), "exec")

        module = types.ModuleType(module_name)
        module.__file__ = str(path)
        exec(code, module.__dict__)  # noqa: S102

        found: Dict[str, Type[BasePlugin]] = {}
        for _attr_name, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, BasePlugin)
                and obj is not BasePlugin
                and obj.name  # must have a non-empty name
            ):
                found[obj.name] = obj

        return found

    def __repr__(self) -> str:
        return f"PluginLoader(plugin_dir={str(self.plugin_dir)!r})"
