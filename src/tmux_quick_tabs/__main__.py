"""Command line entry point for tmux-quick-tabs."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import __version__
from .new_window import run_new_window

__all__ = ["main"]


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser used by :func:`main`."""

    parser = argparse.ArgumentParser(
        prog="tmux-quick-tabs",
        description=(
            "Bootstrap CLI for the tmux-quick-tabs refactor. Later steps will "
            "replace this placeholder with real commands that replicate the "
            "existing shell scripts."
        ),
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")

    new_window_parser = subparsers.add_parser(
        "new-window",
        help="Open a popup that creates a tmux window using shell-style prompts.",
    )
    new_window_parser.set_defaults(func=_run_new_window_command)
    return parser


def _run_new_window_command(_args: argparse.Namespace) -> int:
    """Entrypoint used by the ``new-window`` subcommand."""

    run_new_window()
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the placeholder CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "func", None)
    if handler is not None:
        return handler(args)
    print("tmux-quick-tabs' Python CLI is under construction.")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI execution guard
    raise SystemExit(main())
