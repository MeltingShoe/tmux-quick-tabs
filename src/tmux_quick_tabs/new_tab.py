"""Implementation of the create-new-tab command."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import TYPE_CHECKING

from libtmux import Server

from .dependencies import REQUIRED_EXECUTABLES, warn_missing_dependencies
from .new_window import INITIALIZATION_COMMAND
from .tab_groups import get_or_create_tab_group

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from libtmux.pane import Pane
    from libtmux.session import Session

__all__ = [
    "REQUIRED_EXECUTABLES",
    "POPUP_COMMAND",
    "NewTabCommand",
    "run_new_tab",
]
POPUP_COMMAND = f'tmux send-keys "{INITIALIZATION_COMMAND}" Enter'


@dataclass(slots=True)
class NewTabCommand:
    """Replicate the behaviour of ``scripts/new-tab.sh`` using libtmux."""

    pane: "Pane"
    server: Server | None = None

    def __post_init__(self) -> None:
        if self.server is None:
            self.server = self.pane.session.server  # type: ignore[assignment]

    def run(self) -> None:
        """Execute the command."""

        warn_missing_dependencies(REQUIRED_EXECUTABLES)
        tab_group = get_or_create_tab_group(self.pane)
        active_pane_id = self._active_pane_id()

        new_window = tab_group.new_window(attach=False)
        new_pane = new_window.attached_pane
        if new_pane is None:
            raise RuntimeError("tmux did not return a pane for the new hidden window")
        new_pane_id = new_pane.get("pane_id")
        if not new_pane_id:
            raise RuntimeError("tmux did not provide a pane id for the new hidden window")

        assert self.server is not None  # for type checkers
        self.server.cmd("swap-pane", "-s", active_pane_id, "-t", new_pane_id)
        self.server.cmd("display-popup", "-E", POPUP_COMMAND)
        self._rotate_hidden_windows(tab_group)

    def _active_pane_id(self) -> str:
        pane_id = self.pane.get("pane_id")
        if not pane_id:
            raise RuntimeError("Unable to determine the active pane id")
        return pane_id

    def _rotate_hidden_windows(self, tab_group: "Session") -> None:
        windows = list(tab_group.windows)
        if len(windows) <= 1:
            return
        session_name = tab_group.get("session_name")
        if not session_name:
            raise RuntimeError("tmux did not provide the tab-group session name")
        for index in range(1, len(windows)):
            source = f"{session_name}:{index}"
            target = f"{session_name}:{index + 1}"
            assert self.server is not None
            self.server.cmd("swap-pane", "-s", source, "-t", target)


def _resolve_pane_id(pane_id: str | None) -> str:
    if pane_id:
        return pane_id
    env_pane = os.environ.get("TMUX_PANE")
    if env_pane:
        return env_pane
    raise RuntimeError(
        "tmux-quick-tabs cannot determine the active pane; provide pane_id or set TMUX_PANE."
    )


def _lookup_pane(server: Server, pane_id: str) -> "Pane":
    pane = server.panes.get(pane_id=pane_id, default=None)
    if pane is None:
        raise RuntimeError(f"tmux pane {pane_id!r} not found")
    return pane


def run_new_tab(
    *,
    server: Server | None = None,
    pane: "Pane" | None = None,
    pane_id: str | None = None,
) -> None:
    """Create a new tab for the active tmux pane."""

    if pane is None:
        server = Server() if server is None else server
        pane_id = _resolve_pane_id(pane_id)
        pane = _lookup_pane(server, pane_id)
    else:
        if server is None:
            server = pane.session.server  # type: ignore[assignment]

    command = NewTabCommand(pane=pane, server=server)
    command.run()
