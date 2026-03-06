"""Demonstrates the singleton-registry plugin system.

Run with:
    python examples/main.py   (from the singleton_registry/ directory)
"""

import importlib.util
import pathlib
import sys

# Allow importing from src/ when running the example directly
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

# Import the framework
from singleton_registry import PluginRegistry  # noqa: E402


def _import_file(path: pathlib.Path) -> None:
    """Import a .py file by path so its side-effects (register calls) run."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]


def main() -> None:
    examples_dir = pathlib.Path(__file__).parent

    # Load the example plugins — importing them causes their register() calls
    # to fire, populating the singleton registry.
    for plugin_file in sorted(examples_dir.glob("plugin_*.py")):
        _import_file(plugin_file)

    registry = PluginRegistry()
    print(f"Registered plugins: {list(registry.all().keys())}")
    print()

    for name, plugin_cls in registry.all().items():
        result = plugin_cls().run()
        print(f"  [{name}] → {result}")


if __name__ == "__main__":
    main()
