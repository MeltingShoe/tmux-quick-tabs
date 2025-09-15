from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BINDINGS_PATH = PROJECT_ROOT / "qt-binds.tmux"


@pytest.fixture(scope="module")
def tmux_bindings() -> str:
    return BINDINGS_PATH.read_text()


def test_bindings_reference_python_entrypoints(tmux_bindings: str) -> None:
    assert "-m tmux_quick_tabs" in tmux_bindings
    assert "@quick_tabs_python" in tmux_bindings
    assert "scripts/" not in tmux_bindings
    assert "PYTHONPATH=$SRC_PATH_ESCAPED" in tmux_bindings

    for command in ("new-window", "next-tab", "new-tab", "choose-tab", "close-tab"):
        assert f'"$RUNNER {command}"' in tmux_bindings


def test_bindings_use_display_popup_for_new_window(tmux_bindings: str) -> None:
    assert 'tmux bind c display-popup -E "$RUNNER new-window"' in tmux_bindings


def test_bindings_use_run_shell_for_tab_commands(tmux_bindings: str) -> None:
    assert 'tmux bind-key -n C-n run-shell "$RUNNER next-tab"' in tmux_bindings
    assert 'tmux bind-key -n C-t run-shell "$RUNNER new-tab"' in tmux_bindings
    assert 'tmux bind-key C-n run-shell "$RUNNER choose-tab"' in tmux_bindings
    assert 'tmux bind-key C-t run-shell "$RUNNER close-tab"' in tmux_bindings
