"""Utilities for discovering and creating hidden tab sessions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from libtmux import Pane, Session
    from libtmux.server import Server

__all__ = ["TAB_GROUP_FORMAT", "format_tab_group_name", "get_or_create_tab_group"]

# Matches ``tmux display -p "tabs_#S_#W_#P"`` from the shell implementation.
TAB_GROUP_FORMAT = "tabs_#S_#W_#P"


def format_tab_group_name(pane: "Pane") -> str:
    """Return the hidden session name for *pane*.

    tmux's format expansion rules are mirrored by delegating to
    :meth:`libtmux.Pane.display_message`, which is the programmatic equivalent of
    ``tmux display -p``.
    """

    # ``display_message`` returns either a string or a list of strings depending
    # on the tmux command invoked. ``get_text=True`` matches the ``-p`` flag
    # used by the original shell implementation and avoids printing to the
    # status line.
    message = pane.display_message(TAB_GROUP_FORMAT, get_text=True)
    if isinstance(message, list):
        # When tmux returns a list we only need the first element, which mirrors
        # how ``tmux display -p`` returns the formatted value.
        if not message:
            raise RuntimeError("tmux did not return a tab group name")
        return message[0]
    if not isinstance(message, str):
        raise RuntimeError("Unexpected response from tmux when formatting tab group name")
    return message


def get_or_create_tab_group(pane: "Pane") -> "Session":
    """Return the detached session used to store hidden tabs for *pane*.

    The session mirrors the ``tabs_<session>_<window>_<pane>`` naming scheme
    from the original shell scripts. If the session does not exist it is
    created in a detached state.
    """

    session_name = format_tab_group_name(pane)
    server: "Server" = pane.session.server

    existing_session = server.sessions.get(session_name=session_name, default=None)
    if existing_session is not None:
        return existing_session

    return server.new_session(session_name=session_name, attach=False)

