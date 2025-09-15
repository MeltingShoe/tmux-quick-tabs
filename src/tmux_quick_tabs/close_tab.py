"""Implementation of the close-tab command."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .dependencies import REQUIRED_EXECUTABLES, warn_missing_dependencies
from .tab_groups import format_tab_group_name

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from libtmux import Pane
    from libtmux.server import Server

__all__ = ["ACTIVE_PANE_FORMAT", "CloseTabCommand", "close_tab", "run_close_tab"]

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


def _resolve_pane(server: "Server", pane_id: str | None) -> "Pane":
    if pane_id is None:
        try:
            pane_id = os.environ["TMUX_PANE"]
        except KeyError as exc:  # pragma: no cover - defensive programming
            raise RuntimeError(
                "tmux-quick-tabs cannot determine the active pane; provide pane_id or set TMUX_PANE."
            ) from exc
    pane = server.panes.get(pane_id=pane_id, default=None)
    if pane is None:  # pragma: no cover - defensive programming
        raise RuntimeError(f"tmux pane {pane_id!r} not found")
    return pane


def run_close_tab(
    *,
    server: "Server" | None = None,
    pane: "Pane" | None = None,
    pane_id: str | None = None,
) -> None:
    """Execute the close-tab command for the active tmux pane."""

    if pane is None:
        if server is None:
            from libtmux import Server as LibtmuxServer  # pragma: no cover - imported lazily

            server = LibtmuxServer()
        pane = _resolve_pane(server, pane_id)

    close_tab(pane)
