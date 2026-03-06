"""Tests for the singleton_registry package."""

import pytest

from singleton_registry import BasePlugin, PluginRegistry


@pytest.fixture(autouse=True)
def clean_registry():
    """Ensure the singleton registry is empty before and after each test."""
    registry = PluginRegistry()
    registry._plugins.clear()
    yield
    registry._plugins.clear()


# ---------------------------------------------------------------------------
# PluginRegistry singleton behaviour
# ---------------------------------------------------------------------------


def test_registry_is_singleton():
    r1 = PluginRegistry()
    r2 = PluginRegistry()
    assert r1 is r2


def test_register_and_get():
    class MyPlugin(BasePlugin):
        name = "my_plugin"

        def run(self):
            return "ok"

    PluginRegistry().register("my_plugin", MyPlugin)
    assert PluginRegistry().get("my_plugin") is MyPlugin


def test_get_missing_returns_none():
    assert PluginRegistry().get("does_not_exist") is None


def test_unregister():
    class TempPlugin(BasePlugin):
        name = "temp"

        def run(self):
            return ""

    reg = PluginRegistry()
    reg.register("temp", TempPlugin)
    assert reg.get("temp") is TempPlugin
    reg.unregister("temp")
    assert reg.get("temp") is None


def test_all_returns_copy():
    class P(BasePlugin):
        name = "p"

        def run(self):
            return ""

    reg = PluginRegistry()
    reg.register("p", P)
    snapshot = reg.all()
    snapshot["extra"] = object()
    # Original registry must not be affected
    assert "extra" not in reg.all()


# ---------------------------------------------------------------------------
# BasePlugin.register classmethod
# ---------------------------------------------------------------------------


def test_classmethod_registration():
    class AlphaPlugin(BasePlugin):
        name = "alpha"

        def run(self):
            return "alpha"

    AlphaPlugin.register()
    assert PluginRegistry().get("alpha") is AlphaPlugin


def test_decorator_registration():
    @BasePlugin.register
    class BetaPlugin(BasePlugin):
        name = "beta"

        def run(self):
            return "beta"

    assert PluginRegistry().get("beta") is BetaPlugin


def test_register_returns_class():
    class GammaPlugin(BasePlugin):
        name = "gamma"

        def run(self):
            return "gamma"

    returned = GammaPlugin.register()
    assert returned is GammaPlugin


def test_register_raises_if_name_empty():
    class BadPlugin(BasePlugin):
        name = ""

        def run(self):
            return ""

    with pytest.raises(ValueError, match="non-empty 'name'"):
        BadPlugin.register()


# ---------------------------------------------------------------------------
# BasePlugin interface
# ---------------------------------------------------------------------------


def test_run_not_implemented():
    class IncompletePlugin(BasePlugin):
        name = "incomplete"

    with pytest.raises(NotImplementedError):
        IncompletePlugin().run()


def test_custom_run():
    class HelloPlugin(BasePlugin):
        name = "hello"

        def run(self):
            return "hello!"

    assert HelloPlugin().run() == "hello!"
