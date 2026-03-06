# dynamic_plugins

An example Python plugin system that discovers plugins **dynamically** by scanning a
directory for files with the `.python` extension.

## Concept

No explicit registration is needed.  Drop a `.python` file into the plugin directory
and it is picked up automatically on the next load.  Files whose names begin with an
underscore (`_`) are intentionally skipped so that you can place helpers or
`__init__`-style files alongside the plugins without them being treated as plugins
themselves.

```
plugin_dir/
    hello.python       ← loaded ✔
    goodbye.python     ← loaded ✔
    _helpers.python    ← skipped (leading underscore) ✗
```

Each `.python` file is a regular Python module.  The loader reads, compiles, and
executes it with :func:`compile` + :func:`exec` (Python's standard import machinery
does not handle non-``.py`` extensions), then collects every name that is a
subclass of `BasePlugin`.

> **Security note**: `exec` runs file contents with full process privileges.
> Only point the loader at directories you trust.  Never allow untrusted users
> to write into the plugin directory.

## Installation

```bash
pip install -e .
```

## Quick start

```python
from dynamic_plugins import PluginLoader

loader = PluginLoader("path/to/plugin_dir")
plugins = loader.load()

for name, cls in plugins.items():
    print(name, cls().run())
```

## Writing a plugin

Create a file called `my_plugin.python` inside your plugin directory:

```python
from dynamic_plugins import BasePlugin

class MyPlugin(BasePlugin):
    name = "my_plugin"

    def run(self) -> str:
        return "Hello from MyPlugin!"
```

## Running the example

```bash
python examples/main.py   # from the dynamic_plugins/ directory
```

## Running the tests

```bash
pytest tests/
```
