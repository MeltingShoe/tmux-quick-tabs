from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock, patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from tmux_quick_tabs.choose_tab import (  # noqa: E402  - added to sys.path at runtime
    CHOOSE_TREE_COMMAND,
    CHOOSE_TREE_FORMAT,
    run_choose_tab,
)


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
