# entry_points_plugins

An example Python plugin system that discovers plugins via **`importlib.metadata`
entry points** — the standard mechanism used by tools like `pytest`, `Flask`, and
`Sphinx` for third-party extensions.

## Concept

The host package (`entry_points_plugins`) defines an entry-point **group**
(`"entry_points_plugins.plugins"`).  Any installed package can advertise plugins
by adding entries to that group in its own `pyproject.toml`:

```toml
# In a plugin package's pyproject.toml:
[project.entry-points."entry_points_plugins.plugins"]
my_plugin = "my_package:MyPlugin"
```

The host loader then calls `importlib.metadata.entry_points(group=...)` at runtime
to discover every registered plugin — **without** knowing about the plugin packages
ahead of time.

```
entry_points_plugins.plugins (entry-point group)
    ├── alpha  →  plugin_alpha:AlphaPlugin
    └── beta   →  plugin_beta:BetaPlugin
```

## Installation

```bash
# Install the host package
pip install -e .

# Install the bundled example plugin packages
pip install -e example_plugins/plugin_alpha
pip install -e example_plugins/plugin_beta
```

## Quick start

```python
from entry_points_plugins import PluginLoader

loader = PluginLoader()
plugins = loader.load()

for name, cls in plugins.items():
    print(name, cls().run())
```

## Writing a plugin

1. Create a new Python package (it can be as small as a single module).

2. Define a class that inherits from `BasePlugin`:

   ```python
   # my_awesome_plugin/__init__.py
   from entry_points_plugins import BasePlugin

   class AwesomePlugin(BasePlugin):
       name = "awesome"

       def run(self) -> str:
           return "I am awesome!"
   ```

3. Register it in the package's `pyproject.toml`:

   ```toml
   [project.entry-points."entry_points_plugins.plugins"]
   awesome = "my_awesome_plugin:AwesomePlugin"
   ```

4. Install the package (`pip install -e .`) and it will appear automatically.

## Running the example

```bash
# Install everything first
pip install -e .
pip install -e example_plugins/plugin_alpha
pip install -e example_plugins/plugin_beta

python examples/main.py
```

## Running the tests

```bash
pip install -e ".[dev]" \
    -e example_plugins/plugin_alpha \
    -e example_plugins/plugin_beta
pytest tests/
```
