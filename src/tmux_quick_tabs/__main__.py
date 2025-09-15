"""Command line entry point for tmux-quick-tabs."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from . import __version__

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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the placeholder CLI."""

    parser = build_parser()
    parser.parse_args(argv)
    print("tmux-quick-tabs' Python CLI is under construction.")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI execution guard
    raise SystemExit(main())
