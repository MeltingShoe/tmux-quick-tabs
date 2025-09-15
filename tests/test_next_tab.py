from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock, call

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from tmux_quick_tabs.next_tab import CycleNextTabCommand  # noqa: E402  - added to sys.path at runtime


def make_pane(*, tab_group: str = "tabs_default", pane_id: str = "%1"):
    pane = Mock()
    pane.display_message.return_value = tab_group
    pane.get.return_value = pane_id
    pane.session = Mock()
    server = Mock()
    pane.session.server = server
    sessions = Mock()
    server.sessions = sessions
    return pane, server, sessions


def test_cycle_next_tab_rotates_when_session_exists():
    pane, server, sessions = make_pane(tab_group="tabs_dev_main_1", pane_id="%5")
    session = Mock()
    session.windows = [Mock(), Mock(), Mock()]
    sessions.get.return_value = session

    command = CycleNextTabCommand(pane=pane)
    command.run()

    sessions.get.assert_called_once_with(session_name="tabs_dev_main_1", default=None)
    assert server.cmd.call_args_list == [
        call("swap-pane", "-s", "%5", "-t", "tabs_dev_main_1:1"),
        call("swap-pane", "-s", "tabs_dev_main_1:1", "-t", "tabs_dev_main_1:2"),
        call("swap-pane", "-s", "tabs_dev_main_1:2", "-t", "tabs_dev_main_1:3"),
    ]


def test_cycle_next_tab_creates_missing_session_with_buggy_command():
    pane, server, sessions = make_pane(tab_group="tabs_work_1_0", pane_id="%3")
    session = Mock()
    session.windows = [Mock()]
    sessions.get.side_effect = [None, session]

    command = CycleNextTabCommand(pane=pane)
    command.run()

    assert sessions.get.call_args_list == [
        call(session_name="tabs_work_1_0", default=None),
        call(session_name="tabs_work_1_0", default=None),
    ]
    assert server.cmd.call_args_list == [
        call("new", "-d", "-s", "tabs_work_1_0"),
        call("swap-pane", "-s", "%3", "-t", "tabs_work_1_0:1"),
    ]

