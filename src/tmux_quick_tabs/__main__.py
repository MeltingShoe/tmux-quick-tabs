"""Command line entry point for tmux-quick-tabs."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import __version__
from .choose_tab import run_choose_tab
from .close_tab import run_close_tab
from .new_tab import run_new_tab
from .new_window import run_new_window
from .next_tab import run_cycle_next_tab

__all__ = ["main"]


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser used by :func:`main`."""

    parser = argparse.ArgumentParser(
        prog="tmux-quick-tabs",
        description="Python entrypoints that back the tmux-quick-tabs key bindings.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")

    new_tab_parser = subparsers.add_parser(
        "new-tab",
        help="Create a hidden tab from the active pane and open the init popup.",
    )
    _add_pane_id_argument(new_tab_parser)
    new_tab_parser.set_defaults(func=_run_new_tab_command)

    next_tab_parser = subparsers.add_parser(
        "next-tab",
        help="Swap the active pane into the next stored tab in the hidden session.",
    )
    _add_pane_id_argument(next_tab_parser)
    next_tab_parser.set_defaults(func=_run_next_tab_command)

    choose_tab_parser = subparsers.add_parser(
        "choose-tab",
        help="Open a choose-tree filtered to hidden tabs for the active pane.",
    )
    _add_pane_id_argument(choose_tab_parser)
    choose_tab_parser.set_defaults(func=_run_choose_tab_command)

    close_tab_parser = subparsers.add_parser(
        "close-tab",
        help="Swap the active pane into the tab buffer and kill the stored pane.",
    )
    _add_pane_id_argument(close_tab_parser)
    close_tab_parser.set_defaults(func=_run_close_tab_command)

    new_window_parser = subparsers.add_parser(
        "new-window",
        help="Open a popup that creates a tmux window using shell-style prompts.",
    )
    new_window_parser.set_defaults(func=_run_new_window_command)
    return parser


def _add_pane_id_argument(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "--pane-id",
        help="Identifier of the tmux pane to target. Defaults to $TMUX_PANE when omitted.",
    )


def _run_new_tab_command(args: argparse.Namespace) -> int:
    run_new_tab(pane_id=args.pane_id)
    return 0


def _run_next_tab_command(args: argparse.Namespace) -> int:
    run_cycle_next_tab(pane_id=args.pane_id)
    return 0


def _run_choose_tab_command(args: argparse.Namespace) -> int:
    run_choose_tab(pane_id=args.pane_id)
    return 0


def _run_close_tab_command(args: argparse.Namespace) -> int:
    run_close_tab(pane_id=args.pane_id)
    return 0


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
