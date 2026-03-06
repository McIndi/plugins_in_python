# singleton_registry

An example Python plugin system that uses a **singleton registry** and a **classmethod** for
plugin registration.

## Concept

A single `PluginRegistry` instance (the singleton) holds all registered plugin classes.
`BasePlugin` exposes a `register` classmethod so that any subclass can self-register with
one explicit call — or be used as a decorator.

```
PluginRegistry (singleton)
    └── {"plugin_a": PluginA, "plugin_b": PluginB, ...}

BasePlugin
    └── register(cls)   ← classmethod; writes cls into the singleton
```

## Installation

```bash
pip install -e .
```

## Quick start

```python
from singleton_registry import BasePlugin, PluginRegistry

# Define a plugin
class GreeterPlugin(BasePlugin):
    name = "greeter"

    def run(self, subject: str) -> str:
        return f"Hello, {subject}!"

# Register it
GreeterPlugin.register()

# Retrieve and use it
registry = PluginRegistry()
plugin_cls = registry.get("greeter")
print(plugin_cls().run("world"))   # Hello, world!
```

Alternatively use `register` as a **decorator**:

```python
@BasePlugin.register
class GreeterPlugin(BasePlugin):
    name = "greeter"

    def run(self, subject: str) -> str:
        return f"Hello, {subject}!"
```

## Running the example

```bash
python examples/main.py
```

## Running the tests

```bash
pytest tests/
```
