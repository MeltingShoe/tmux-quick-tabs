"""Implementation of the cycle-to-next-tab command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .tab_groups import format_tab_group_name

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from libtmux import Pane, Session
    from libtmux.server import Server

__all__ = ["CycleNextTabCommand", "cycle_next_tab"]


@dataclass(slots=True)
class CycleNextTabCommand:
    """Swap the active pane into the next hidden tab and rotate the buffer."""

    pane: "Pane"

    def run(self) -> None:
        """Execute the command."""

        tab_group = format_tab_group_name(self.pane)
        pane_id = self._get_active_pane_id()
        server: "Server" = self.pane.session.server

        session = server.sessions.get(session_name=tab_group, default=None)
        if session is None:
            # Mirrors the original bug where ``tmux new`` is used instead of
            # ``new-session``.  The call may fail to create the session which is
            # why we attempt to fetch it again afterwards instead of assuming
            # success.
            server.cmd("new", "-d", "-s", tab_group)
            session = server.sessions.get(session_name=tab_group, default=None)

        # The swap-pane call is always attempted, even if the hidden session
        # does not exist, matching the behaviour of the original shell script.
        server.cmd("swap-pane", "-s", pane_id, "-t", f"{tab_group}:1")

        if session is None:
            return

        self._rotate_hidden_windows(server=server, tab_group=tab_group, session=session)

    def _get_active_pane_id(self) -> str:
        pane_id = self.pane.get("pane_id")
        if not pane_id:
            pane_id = getattr(self.pane, "pane_id", None)
        if not pane_id:
            raise RuntimeError("Unable to determine active pane id")
        return pane_id

    def _rotate_hidden_windows(
        self,
        *,
        server: "Server",
        tab_group: str,
        session: "Session",
    ) -> None:
        windows = list(getattr(session, "windows", []))
        if len(windows) <= 1:
            return

        # Window indexes in the hidden session start at 1.  Rotation mirrors the
        # shell implementation by swapping ``tab_group:i`` with ``tab_group:i+1``
        # for the range ``[1, buffer_len)``.
        for index in range(1, len(windows)):
            server.cmd(
                "swap-pane",
                "-s",
                f"{tab_group}:{index}",
                "-t",
                f"{tab_group}:{index + 1}",
            )


def cycle_next_tab(pane: "Pane") -> None:
    """Convenience wrapper that executes :class:`CycleNextTabCommand`."""

    CycleNextTabCommand(pane=pane).run()

