"""Demonstrates the dynamic file-based plugin system.

Run with:
    python examples/main.py   (from the dynamic_plugins/ directory)
"""

import pathlib
import sys

# Allow importing from src/ when running the example directly
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

from dynamic_plugins import PluginLoader  # noqa: E402

PLUGIN_DIR = pathlib.Path(__file__).parent.parent / "example_plugins"


def main() -> None:
    loader = PluginLoader(PLUGIN_DIR)
    plugins = loader.load()

    print(f"Discovered {len(plugins)} plugin(s) in '{PLUGIN_DIR.name}/':")
    for name, plugin_cls in plugins.items():
        result = plugin_cls().run()
        print(f"  [{name}] → {result}")


if __name__ == "__main__":
    main()
