from __future__ import annotations

import os
import sys
import types
from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

try:  # pragma: no cover - fallback for environments without libtmux
    from libtmux import Server  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - executed only in CI where libtmux missing
    libtmux_module = types.ModuleType("libtmux")

    class Server:  # type: ignore[too-many-ancestors]
        """Minimal stub used when libtmux is unavailable during tests."""

        panes: Mock

        def __init__(self) -> None:  # pragma: no cover - not used
            self.panes = Mock()

        def cmd(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - not used
            raise NotImplementedError

    sys.modules["libtmux"] = libtmux_module
    libtmux_module.Server = Server

from tmux_quick_tabs.new_tab import (  # noqa: E402  - added to sys.path at runtime
    POPUP_COMMAND,
    run_new_tab,
)


def make_pane(server: Mock, pane_id: str = "%1") -> Mock:
    pane = Mock()
    pane.get.side_effect = lambda key: {"pane_id": pane_id}[key]
    pane.session = Mock()
    pane.session.server = server
    return pane


def test_run_new_tab_swaps_panes_opens_popup_and_rotates(monkeypatch: pytest.MonkeyPatch):
    server = Mock(spec=["cmd", "panes"])
    pane = make_pane(server, "%3")

    tab_group = Mock()
    new_window = Mock()
    new_pane = Mock()
    new_pane.get.return_value = "%7"
    new_window.attached_pane = new_pane
    tab_group.new_window.return_value = new_window
    tab_group.windows = [Mock(), Mock(), Mock()]
    tab_group.get.return_value = "tabs_dev_1_1"

    monkeypatch.setattr(
        "tmux_quick_tabs.new_tab.get_or_create_tab_group", lambda p: tab_group
    )
    monkeypatch.setattr("tmux_quick_tabs.new_tab.shutil.which", lambda name: f"/usr/bin/{name}")

    run_new_tab(server=server, pane=pane)

    tab_group.new_window.assert_called_once_with(attach=False)
    assert server.cmd.call_args_list == [
        call("swap-pane", "-s", "%3", "-t", "%7"),
        call("display-popup", "-E", POPUP_COMMAND),
        call("swap-pane", "-s", "tabs_dev_1_1:1", "-t", "tabs_dev_1_1:2"),
        call("swap-pane", "-s", "tabs_dev_1_1:2", "-t", "tabs_dev_1_1:3"),
    ]


def test_run_new_tab_skips_rotation_with_single_hidden_window(monkeypatch: pytest.MonkeyPatch):
    server = Mock(spec=["cmd", "panes"])
    pane = make_pane(server)

    tab_group = Mock()
    new_window = Mock()
    new_pane = Mock()
    new_pane.get.return_value = "%8"
    new_window.attached_pane = new_pane
    tab_group.new_window.return_value = new_window
    tab_group.windows = [Mock()]
    tab_group.get.return_value = "tabs_example"

    monkeypatch.setattr(
        "tmux_quick_tabs.new_tab.get_or_create_tab_group", lambda p: tab_group
    )
    monkeypatch.setattr("tmux_quick_tabs.new_tab.shutil.which", lambda name: f"/usr/bin/{name}")

    run_new_tab(server=server, pane=pane)

    assert server.cmd.call_args_list == [
        call("swap-pane", "-s", "%1", "-t", "%8"),
        call("display-popup", "-E", POPUP_COMMAND),
    ]


def test_run_new_tab_fails_when_dependencies_missing(monkeypatch: pytest.MonkeyPatch):
    server = Mock(spec=["cmd", "panes"])
    pane = make_pane(server)

    monkeypatch.setattr(
        "tmux_quick_tabs.new_tab.shutil.which",
        lambda name: None if name == "zoxide" else f"/usr/bin/{name}",
    )

    with pytest.raises(RuntimeError) as excinfo:
        run_new_tab(server=server, pane=pane)

    server.cmd.assert_not_called()
    message = str(excinfo.value)
    assert "Missing required dependencies" in message
    assert "zoxide" in message
    assert "fzf" not in message


def test_run_new_tab_resolves_active_pane_from_server(monkeypatch: pytest.MonkeyPatch):
    server = Mock()
    server.cmd = Mock()
    server.panes = Mock()
    server.panes.get.return_value = pane = make_pane(server, "%9")

    tab_group = Mock()
    new_window = Mock()
    new_pane = Mock()
    new_pane.get.return_value = "%10"
    new_window.attached_pane = new_pane
    tab_group.new_window.return_value = new_window
    tab_group.windows = [Mock(), Mock()]
    tab_group.get.return_value = "tabs_work"

    monkeypatch.setattr(
        "tmux_quick_tabs.new_tab.get_or_create_tab_group", lambda p: tab_group
    )
    monkeypatch.setattr("tmux_quick_tabs.new_tab.shutil.which", lambda name: f"/usr/bin/{name}")

    with patch.dict(os.environ, {"TMUX_PANE": "%9"}, clear=False):
        run_new_tab(server=server)

    server.panes.get.assert_called_once_with(pane_id="%9", default=None)
    assert server.cmd.call_args_list[0] == call("swap-pane", "-s", "%9", "-t", "%10")
