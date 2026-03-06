"""Demonstrates the entry-point plugin system.

Run with:
    # First install everything:
    pip install -e .
    pip install -e example_plugins/plugin_alpha
    pip install -e example_plugins/plugin_beta

    # Then run:
    python examples/main.py   (from the entry_points_plugins/ directory)
"""

from entry_points_plugins import PluginLoader


def main() -> None:
    loader = PluginLoader()
    plugins = loader.load()

    if not plugins:
        print(
            "No plugins found.  Make sure you have installed the example plugins:\n"
            "  pip install -e example_plugins/plugin_alpha\n"
            "  pip install -e example_plugins/plugin_beta"
        )
        return

    print(f"Discovered {len(plugins)} plugin(s) via entry_points:")
    for name, plugin_cls in plugins.items():
        result = plugin_cls().run()
        print(f"  [{name}] → {result}")


if __name__ == "__main__":
    main()
