"""Implementation of the choose-tab tree command."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING


from libtmux import Server

from .dependencies import REQUIRED_EXECUTABLES, warn_missing_dependencies
from .tab_groups import format_tab_group_name, get_or_create_tab_group

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from libtmux import Pane, Server

__all__ = [
    "CHOOSE_TREE_COMMAND",
    "CHOOSE_TREE_FORMAT",
    "ChooseTabCommand",
    "run_choose_tab",
]

CHOOSE_TREE_FORMAT = "#{pane_title} #{pane_current_command} #{pane_current_path}"
CHOOSE_TREE_COMMAND = "swap-pane -t '%%'"


def _build_session_filter(session_name: str) -> str:
    """Return the choose-tree filter targeting *session_name*."""

    return f"#{{==:#{{session_name}},{session_name}}}"


@dataclass(slots=True)
class ChooseTabCommand:
    """Invoke choose-tree restricted to panes inside the hidden tab session."""

    pane: "Pane"

    def run(self) -> None:
        """Execute the command."""

        warn_missing_dependencies(REQUIRED_EXECUTABLES)
        tab_group = get_or_create_tab_group(self.pane)
        session_name = None
        if hasattr(tab_group, "get"):
            session_name = tab_group.get("session_name")
        if not session_name:
            session_name = format_tab_group_name(self.pane)
        self.pane.cmd(
            "choose-tree",
            "-F",
            CHOOSE_TREE_FORMAT,
            "-f",
            _build_session_filter(session_name),
            CHOOSE_TREE_COMMAND,
        )


def _resolve_pane(server: "Server", pane_id: str | None) -> "Pane":
    """Return the tmux pane identified by *pane_id*."""

    if pane_id is None:
        try:
            pane_id = os.environ["TMUX_PANE"]
        except KeyError as exc:  # pragma: no cover - defensive programming
            raise RuntimeError(
                "TMUX_PANE environment variable is not set and no pane_id was provided"
            ) from exc
    pane = server.panes.get(pane_id=pane_id, default=None)
    if pane is None:  # pragma: no cover - defensive programming
        raise RuntimeError(f"Unable to locate pane {pane_id!r} on the tmux server")
    return pane


def run_choose_tab(
    *,
    server: "Server" | None = None,
    pane: "Pane" | None = None,
    pane_id: str | None = None,
) -> None:
    """Run the choose-tab command for *pane* or the active tmux pane."""

    if pane is None:
        if server is None:
            from libtmux import Server as LibtmuxServer  # pragma: no cover - imported lazily

            server = LibtmuxServer()
        pane = _resolve_pane(server, pane_id)
    else:
        if server is None:
            server = getattr(pane.session, "server", None)
        if server is None:  # pragma: no cover - defensive programming
            raise RuntimeError("The provided pane is not associated with a tmux server")
    command = ChooseTabCommand(pane=pane)
    command.run()
