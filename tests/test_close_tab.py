from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock, call

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from tmux_quick_tabs.close_tab import (  # noqa: E402  - added to sys.path at runtime
    ACTIVE_PANE_FORMAT,
    close_tab,
)
from tmux_quick_tabs.dependencies import DependencyWarning  # noqa: E402  - added to sys.path at runtime
from tmux_quick_tabs.tab_groups import TAB_GROUP_FORMAT  # noqa: E402  - added to sys.path at runtime


def make_pane(*, tab_group: str = "tabs_main_dev_1", pane_id: str = "%0"):
    pane = Mock()
    server = Mock()
    sessions = Mock()
    server.sessions = sessions
    pane.session = Mock()
    pane.session.server = server

    def display_message(format_string: str, get_text: bool = True):
        if format_string == TAB_GROUP_FORMAT:
            return tab_group
        if format_string == ACTIVE_PANE_FORMAT:
            return pane_id
        raise AssertionError(f"Unexpected format string: {format_string}")

    pane.display_message.side_effect = display_message
    return pane, server, sessions


def test_close_tab_kills_active_pane_when_hidden_session_missing():
    pane, server, sessions = make_pane(tab_group="tabs_alpha", pane_id="%5")
    sessions.get.return_value = None

    close_tab(pane)

    pane.display_message.assert_any_call(TAB_GROUP_FORMAT, get_text=True)
    pane.display_message.assert_any_call(ACTIVE_PANE_FORMAT, get_text=True)
    sessions.get.assert_called_once_with(session_name="tabs_alpha", default=None)
    server.cmd.assert_called_once_with("kill-pane", "-t", "%5")


def test_close_tab_swaps_and_kills_hidden_pane():
    pane, server, sessions = make_pane(tab_group="tabs_work_main", pane_id="%3")
    hidden_session = Mock()
    sessions.get.return_value = hidden_session

    close_tab(pane)

    assert server.cmd.call_args_list == [
        call("swap-pane", "-t", "tabs_work_main:1"),
        call("kill-pane", "-t", "tabs_work_main:1"),
    ]


def test_close_tab_keeps_hidden_session_alive_when_empty():
    pane, server, sessions = make_pane(tab_group="tabs_empty", pane_id="%7")
    hidden_session = Mock()
    hidden_session.windows = []
    sessions.get.return_value = hidden_session

    close_tab(pane)

    hidden_session.kill_session.assert_not_called()
    for recorded_call in server.cmd.call_args_list:
        assert recorded_call.args[0] != "kill-session"


def test_close_tab_supports_list_output_for_active_pane_id():
    pane, server, sessions = make_pane(tab_group="tabs_list")

    def display_message(format_string: str, get_text: bool = True):
        if format_string == TAB_GROUP_FORMAT:
            return "tabs_list"
        if format_string == ACTIVE_PANE_FORMAT:
            return ["%9"]
        raise AssertionError(f"Unexpected format string: {format_string}")

    pane.display_message.side_effect = display_message
    sessions.get.return_value = None

    close_tab(pane)

    server.cmd.assert_called_once_with("kill-pane", "-t", "%9")


def test_close_tab_warns_about_missing_dependencies(monkeypatch: pytest.MonkeyPatch):
    pane, server, sessions = make_pane(tab_group="tabs_warn_close", pane_id="%6")
    sessions.get.return_value = None

    monkeypatch.setattr("tmux_quick_tabs.dependencies.shutil.which", lambda name: None)

    with pytest.warns(DependencyWarning) as record:
        close_tab(pane)

    server.cmd.assert_called_once_with("kill-pane", "-t", "%6")
    assert record
