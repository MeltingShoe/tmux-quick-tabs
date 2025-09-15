"""Utilities for validating external command dependencies."""

from __future__ import annotations

import shutil
import warnings
from typing import Iterable, Tuple

__all__ = [
    "DependencyWarning",
    "REQUIRED_EXECUTABLES",
    "find_missing_dependencies",
    "warn_missing_dependencies",
]


class DependencyWarning(UserWarning):
    """Warning raised when optional tmux-quick-tabs dependencies are missing."""


REQUIRED_EXECUTABLES: Tuple[str, ...] = ("zoxide", "fzf")


def find_missing_dependencies(
    names: Iterable[str] = REQUIRED_EXECUTABLES,
) -> tuple[str, ...]:
    """Return a tuple of dependency names that are not available on ``PATH``."""

    missing = tuple(sorted(name for name in names if shutil.which(name) is None))
    return missing


def warn_missing_dependencies(
    names: Iterable[str] = REQUIRED_EXECUTABLES,
) -> tuple[str, ...]:
    """Warn about missing dependencies while allowing execution to continue."""

    missing = find_missing_dependencies(names)
    if missing:
        dependency_list = ", ".join(missing)
        warnings.warn(
            f"Missing optional dependencies for tmux-quick-tabs: {dependency_list}.",
            DependencyWarning,
            stacklevel=2,
        )
    return missing

