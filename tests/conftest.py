"""Shared pytest fixtures for tmux-quick-tabs tests."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _mock_dependency_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pretend required executables are present unless a test overrides it."""

    monkeypatch.setattr(
        "tmux_quick_tabs.dependencies.shutil.which",
        lambda name: f"/usr/bin/{name}",
    )
