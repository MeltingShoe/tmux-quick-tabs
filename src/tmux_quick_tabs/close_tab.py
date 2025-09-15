"""Implementation of the close-tab command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .dependencies import REQUIRED_EXECUTABLES, warn_missing_dependencies
from .tab_groups import format_tab_group_name

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from libtmux import Pane

__all__ = ["ACTIVE_PANE_FORMAT", "CloseTabCommand", "close_tab"]

# Matches ``tmux display -p "#{pane_id}"`` from the shell implementation.
ACTIVE_PANE_FORMAT = "#{pane_id}"


def _format_active_pane_id(pane: "Pane") -> str:
    """Return the active pane id for *pane*."""

    message = pane.display_message(ACTIVE_PANE_FORMAT, get_text=True)
    if isinstance(message, list):
        if not message:
            raise RuntimeError("tmux did not return an active pane id")
        return message[0]
    if not isinstance(message, str):
        raise RuntimeError("Unexpected response from tmux when formatting active pane id")
    return message


@dataclass(slots=True)
class CloseTabCommand:
    """Swap the active pane into the hidden session and kill it."""

    pane: "Pane"

    def run(self) -> None:
        """Execute the close-tab command."""

        warn_missing_dependencies(REQUIRED_EXECUTABLES)
        tab_group_name = format_tab_group_name(self.pane)
        active_pane_id = _format_active_pane_id(self.pane)
        server = self.pane.session.server

        hidden_session = server.sessions.get(session_name=tab_group_name, default=None)
        if hidden_session is None:
            server.cmd("kill-pane", "-t", active_pane_id)
            return

        # Mirrors ``tmux swap-pane -t $tab_group:1`` which implicitly swaps the
        # active pane with the hidden pane. No rotation occurs for this command.
        server.cmd("swap-pane", "-t", f"{tab_group_name}:1")
        server.cmd("kill-pane", "-t", f"{tab_group_name}:1")
        # Intentionally leave the hidden session running even if no panes remain,
        # matching the original shell implementation's leak.


def close_tab(pane: "Pane") -> None:
    """Convenience wrapper around :class:`CloseTabCommand`."""

    CloseTabCommand(pane=pane).run()
