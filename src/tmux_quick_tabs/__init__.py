"""tmux-quick-tabs Python package."""

from __future__ import annotations

__all__ = ["__version__"]

# NOTE: The version is defined here instead of dynamically deriving it so that
# importing :mod:`tmux_quick_tabs` has no side effects during early
# bootstrapping of the refactor. Later steps can update this value when the
# Python implementation becomes feature complete.
__version__ = "0.1.0"
