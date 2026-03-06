"""Tests for the dynamic_plugins package."""

import pathlib
import textwrap

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SRC = pathlib.Path(__file__).parent.parent / "src"


@pytest.fixture(autouse=True)
def add_src_to_path(monkeypatch):
    """Ensure the package can be imported without installing it."""
    import sys

    monkeypatch.syspath_prepend(str(SRC))


@pytest.fixture()
def plugin_dir(tmp_path):
    """Return a temporary directory pre-populated with test plugins."""
    return tmp_path


def write_plugin(directory: pathlib.Path, filename: str, content: str) -> pathlib.Path:
    path = directory / filename
    path.write_text(textwrap.dedent(content))
    return path


# ---------------------------------------------------------------------------
# PluginLoader — discovery
# ---------------------------------------------------------------------------


def test_loads_dot_python_files(plugin_dir):
    write_plugin(
        plugin_dir,
        "greet.python",
        """\
        from dynamic_plugins import BasePlugin

        class GreetPlugin(BasePlugin):
            name = "greet"
            def run(self):
                return "hi"
        """,
    )

    from dynamic_plugins import PluginLoader

    plugins = PluginLoader(plugin_dir).load()
    assert "greet" in plugins
    assert plugins["greet"]().run() == "hi"


def test_skips_files_with_leading_underscore(plugin_dir):
    write_plugin(
        plugin_dir,
        "_private.python",
        """\
        from dynamic_plugins import BasePlugin

        class PrivatePlugin(BasePlugin):
            name = "private"
            def run(self):
                return "secret"
        """,
    )

    from dynamic_plugins import PluginLoader

    plugins = PluginLoader(plugin_dir).load()
    assert "private" not in plugins


def test_ignores_non_dot_python_files(plugin_dir):
    (plugin_dir / "helper.py").write_text("x = 1")

    from dynamic_plugins import PluginLoader

    plugins = PluginLoader(plugin_dir).load()
    assert plugins == {}


def test_multiple_plugins_in_same_file(plugin_dir):
    write_plugin(
        plugin_dir,
        "multi.python",
        """\
        from dynamic_plugins import BasePlugin

        class AlphaPlugin(BasePlugin):
            name = "alpha"
            def run(self):
                return "alpha"

        class BetaPlugin(BasePlugin):
            name = "beta"
            def run(self):
                return "beta"
        """,
    )

    from dynamic_plugins import PluginLoader

    plugins = PluginLoader(plugin_dir).load()
    assert set(plugins.keys()) == {"alpha", "beta"}


def test_skips_class_without_name(plugin_dir):
    write_plugin(
        plugin_dir,
        "noname.python",
        """\
        from dynamic_plugins import BasePlugin

        class NoNamePlugin(BasePlugin):
            # name intentionally left empty
            def run(self):
                return "x"
        """,
    )

    from dynamic_plugins import PluginLoader

    plugins = PluginLoader(plugin_dir).load()
    assert plugins == {}


def test_empty_directory(plugin_dir):
    from dynamic_plugins import PluginLoader

    plugins = PluginLoader(plugin_dir).load()
    assert plugins == {}


def test_loads_multiple_files(plugin_dir):
    for letter in ("a", "b", "c"):
        write_plugin(
            plugin_dir,
            f"{letter}.python",
            f"""\
            from dynamic_plugins import BasePlugin

            class Plugin{letter.upper()}(BasePlugin):
                name = "{letter}"
                def run(self):
                    return "{letter}"
            """,
        )

    from dynamic_plugins import PluginLoader

    plugins = PluginLoader(plugin_dir).load()
    assert set(plugins.keys()) == {"a", "b", "c"}


# ---------------------------------------------------------------------------
# BasePlugin interface
# ---------------------------------------------------------------------------


def test_base_plugin_run_raises():
    from dynamic_plugins import BasePlugin

    with pytest.raises(NotImplementedError):
        BasePlugin().run()
