"""Tests for the entry_points_plugins package."""

from __future__ import annotations

from typing import Type
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_entry_point(name: str, plugin_cls: Type) -> MagicMock:
    """Return a mock EntryPoint that loads *plugin_cls* when called."""
    ep = MagicMock()
    ep.name = name
    ep.load.return_value = plugin_cls
    return ep


# ---------------------------------------------------------------------------
# PluginLoader
# ---------------------------------------------------------------------------


def test_load_returns_dict(tmp_path):
    """load() must return a dict even when no plugins are registered."""
    from entry_points_plugins import PluginLoader

    with patch("entry_points_plugins.loader.entry_points", return_value=[]):
        plugins = PluginLoader().load()

    assert isinstance(plugins, dict)
    assert plugins == {}


def test_load_discovers_installed_plugins():
    from entry_points_plugins import BasePlugin, PluginLoader

    class FakePlugin(BasePlugin):
        name = "fake"

        def run(self):
            return "fake"

    eps = [make_entry_point("fake", FakePlugin)]

    with patch("entry_points_plugins.loader.entry_points", return_value=eps):
        plugins = PluginLoader().load()

    assert "fake" in plugins
    assert plugins["fake"] is FakePlugin


def test_load_multiple_plugins():
    from entry_points_plugins import BasePlugin, PluginLoader

    class P1(BasePlugin):
        name = "p1"

        def run(self):
            return "p1"

    class P2(BasePlugin):
        name = "p2"

        def run(self):
            return "p2"

    eps = [make_entry_point("p1", P1), make_entry_point("p2", P2)]

    with patch("entry_points_plugins.loader.entry_points", return_value=eps):
        plugins = PluginLoader().load()

    assert set(plugins.keys()) == {"p1", "p2"}
    assert plugins["p1"] is P1
    assert plugins["p2"] is P2


def test_custom_group():
    from entry_points_plugins import PluginLoader

    loader = PluginLoader(group="my.custom.group")
    assert loader.group == "my.custom.group"

    with patch("entry_points_plugins.loader.entry_points", return_value=[]) as mock_ep:
        loader.load()

    mock_ep.assert_called_once_with(group="my.custom.group")


# ---------------------------------------------------------------------------
# BasePlugin interface
# ---------------------------------------------------------------------------


def test_base_plugin_run_raises():
    from entry_points_plugins import BasePlugin

    with pytest.raises(NotImplementedError):
        BasePlugin().run()


def test_plugin_run():
    from entry_points_plugins import BasePlugin

    class ConcretePlugin(BasePlugin):
        name = "concrete"

        def run(self):
            return "concrete result"

    assert ConcretePlugin().run() == "concrete result"
