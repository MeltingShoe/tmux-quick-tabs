from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from tmux_quick_tabs.tab_groups import (  # noqa: E402  - added to sys.path at runtime
    TAB_GROUP_FORMAT,
    get_or_create_tab_group,
)


def make_pane(*, session_name: str = "tabs_default"):
    pane = Mock()
    server = Mock()
    sessions = Mock()
    server.sessions = sessions
    pane.session = Mock()
    pane.session.server = server
    pane.display_message.return_value = session_name
    return pane, server, sessions


def test_get_or_create_tab_group_creates_missing_session():
    pane, server, sessions = make_pane(session_name="tabs_main_dev_1")
    created_session = Mock()
    sessions.get.return_value = None
    server.new_session.return_value = created_session

    result = get_or_create_tab_group(pane)

    pane.display_message.assert_called_once_with(TAB_GROUP_FORMAT, get_text=True)
    sessions.get.assert_called_once_with(
        session_name="tabs_main_dev_1", default=None
    )
    server.new_session.assert_called_once_with(
        session_name="tabs_main_dev_1", attach=False
    )
    assert result is created_session


def test_get_or_create_tab_group_returns_existing_session():
    pane, server, sessions = make_pane(session_name="tabs_work_2_0")
    existing_session = Mock()
    sessions.get.return_value = existing_session

    result = get_or_create_tab_group(pane)

    server.new_session.assert_not_called()
    assert result is existing_session


def test_get_or_create_tab_group_supports_list_output_from_tmux():
    pane, server, sessions = make_pane()
    pane.display_message.return_value = ["tabs_dev_1_3"]
    existing_session = Mock()
    sessions.get.return_value = existing_session

    result = get_or_create_tab_group(pane)

    sessions.get.assert_called_once_with(
        session_name="tabs_dev_1_3", default=None
    )
    server.new_session.assert_not_called()
    assert result is existing_session
