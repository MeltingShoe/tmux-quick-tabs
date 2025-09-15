from __future__ import annotations

import os
import sys
import types
from pathlib import Path
from unittest.mock import Mock, patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

try:  # pragma: no cover - fallback when libtmux missing
    from libtmux import Server  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - executed only in CI where libtmux missing
    libtmux_module = types.ModuleType("libtmux")

    class Server:  # type: ignore[too-many-ancestors]
        """Minimal stub used when libtmux is unavailable during tests."""

        def cmd(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - not used
            raise NotImplementedError

    libtmux_module.Server = Server
    libtmux_module.__path__ = []  # type: ignore[attr-defined]
    sys.modules["libtmux"] = libtmux_module

import pytest

from tmux_quick_tabs.choose_tab import (  # noqa: E402  - added to sys.path at runtime
    CHOOSE_TREE_COMMAND,
    CHOOSE_TREE_FORMAT,
    run_choose_tab,
)
from tmux_quick_tabs.dependencies import DependencyWarning  # noqa: E402  - added to sys.path at runtime


def make_server_and_pane():
    server = Mock()
    server.panes = Mock()
    pane = Mock()
    pane.session = Mock()
    pane.session.server = server
    server.panes.get.return_value = pane
    return server, pane


def test_run_choose_tab_invokes_choose_tree_with_expected_arguments():
    server, pane = make_server_and_pane()
    tab_session = Mock()
    tab_session.get.return_value = "tabs_main_dev_1"

    with patch("tmux_quick_tabs.choose_tab.get_or_create_tab_group", return_value=tab_session) as get_group:
        run_choose_tab(server=server, pane_id="@7")

    server.panes.get.assert_called_once_with(pane_id="@7", default=None)
    get_group.assert_called_once_with(pane)
    tab_session.get.assert_called_once_with("session_name")
    pane.cmd.assert_called_once_with(
        "choose-tree",
        "-F",
        CHOOSE_TREE_FORMAT,
        "-f",
        "#{==:#{session_name},tabs_main_dev_1}",
        CHOOSE_TREE_COMMAND,
    )


class FakePane:
    def __init__(self, server: Mock, selection: str):
        self.session = Mock()
        self.session.server = server
        self._selection = selection
        self.calls: list[tuple[object, ...]] = []

    def cmd(self, *args):
        self.calls.append(args)
        assert args[0] == "choose-tree"
        command_string = args[-1]
        assert command_string == CHOOSE_TREE_COMMAND
        self.session.server.cmd("swap-pane", "-t", self._selection)
        return []


def test_run_choose_tab_swaps_active_pane_with_chosen_target():
    server = Mock()
    server.panes = Mock()
    selection = "tabs_session:1.0"
    pane = FakePane(server=server, selection=selection)
    server.panes.get.return_value = pane
    tab_session = Mock()
    tab_session.get.return_value = "tabs_session_1_0"

    with patch("tmux_quick_tabs.choose_tab.get_or_create_tab_group", return_value=tab_session):
        run_choose_tab(server=server, pane_id="@3")

    server.cmd.assert_called_once_with("swap-pane", "-t", selection)
    assert pane.calls == [
        (
            "choose-tree",
            "-F",
            CHOOSE_TREE_FORMAT,
            "-f",
            "#{==:#{session_name},tabs_session_1_0}",
            CHOOSE_TREE_COMMAND,
        )
    ]


def test_run_choose_tab_warns_about_missing_dependencies(monkeypatch: pytest.MonkeyPatch):
    server, pane = make_server_and_pane()
    tab_session = Mock()
    tab_session.get.return_value = "tabs_dep_warn"

    monkeypatch.setattr(
        "tmux_quick_tabs.choose_tab.get_or_create_tab_group",
        lambda p: tab_session,
    )
    monkeypatch.setattr("tmux_quick_tabs.dependencies.shutil.which", lambda name: None)

    with pytest.warns(DependencyWarning) as record:
        run_choose_tab(server=server, pane_id="@9")

    pane.cmd.assert_called_once()
    assert record


def test_run_choose_tab_resolves_pane_id_from_environment(monkeypatch: pytest.MonkeyPatch):
    server, pane = make_server_and_pane()
    pane.cmd.return_value = []
    tab_session = Mock()
    tab_session.get.return_value = "tabs_env"

    monkeypatch.setattr(
        "tmux_quick_tabs.choose_tab.get_or_create_tab_group",
        lambda p: tab_session,
    )
    monkeypatch.setitem(os.environ, "TMUX_PANE", "@42")

    run_choose_tab(server=server)

    server.panes.get.assert_called_once_with(pane_id="@42", default=None)
    pane.cmd.assert_called_once()
