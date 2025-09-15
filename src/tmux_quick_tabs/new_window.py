"""Implementation of the new-window popup command."""

from __future__ import annotations

from dataclasses import dataclass
import sys
from typing import TextIO

from libtmux import Server
from libtmux.exc import LibTmuxException

__all__ = [
    "INITIALIZATION_COMMAND",
    "NewWindowCommand",
    "run_new_window",
]

INITIALIZATION_COMMAND = "cd $(zoxide query -l | fzf); clear; ls -a"


@dataclass(slots=True)
class NewWindowCommand:
    """Handle prompting for a new window name and initialisation."""

    server: Server
    stdin: TextIO
    stdout: TextIO

    def prompt(self) -> str:
        """Prompt the user for the window name."""

        print("Enter window name:", file=self.stdout)
        self.stdout.flush()
        line = self.stdin.readline()
        if line.endswith("\n"):
            line = line[:-1]
        return line

    def _split_name(self, name: str) -> list[str]:
        """Replicate shell word-splitting for the provided *name*."""

        return name.split()

    def run(self) -> None:
        """Execute the command to create the window and send the init command."""

        name = self.prompt()
        args = self._split_name(name)
        try:
            self.server.cmd("neww", "-n", *args)
        except LibTmuxException:
            # Mirrors the shell script behaviour which ignores tmux failures and
            # proceeds to send the initialisation command regardless.
            pass
        self.server.cmd("send-keys", INITIALIZATION_COMMAND, "Enter")


def run_new_window(
    *,
    server: Server | None = None,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
) -> None:
    """Run the new-window popup command."""

    server = Server() if server is None else server
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    command = NewWindowCommand(server=server, stdin=stdin, stdout=stdout)
    command.run()
