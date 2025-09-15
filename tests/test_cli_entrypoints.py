from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

try:  # pragma: no cover - exercised only when libtmux missing
    import libtmux  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - executed in CI without libtmux
    import types

    libtmux_module = types.ModuleType("libtmux")

    class Server:  # type: ignore[too-many-ancestors]
        """Minimal stub providing the methods used by the CLI tests."""

        def cmd(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - not used
            raise NotImplementedError

    libtmux_module.Server = Server
    exc_module = types.ModuleType("libtmux.exc")

    class LibTmuxException(Exception):
        """Stub exception mirroring libtmux.exc.LibTmuxException."""

    exc_module.LibTmuxException = LibTmuxException
    libtmux_module.exc = exc_module
    sys.modules["libtmux"] = libtmux_module
    sys.modules["libtmux.exc"] = exc_module

from tmux_quick_tabs import __main__ as cli  # noqa: E402  - added to sys.path at runtime


@pytest.mark.parametrize(
    ("command", "attribute"),
    [
        ("new-tab", "run_new_tab"),
        ("next-tab", "run_cycle_next_tab"),
        ("choose-tab", "run_choose_tab"),
        ("close-tab", "run_close_tab"),
    ],
)
@pytest.mark.parametrize("pane_id", [None, "%9"])
def test_main_invokes_pane_scoped_commands(
    monkeypatch: pytest.MonkeyPatch, command: str, attribute: str, pane_id: str | None
) -> None:
    calls: list[str | None] = []
    monkeypatch.setattr(cli, attribute, lambda *, pane_id=None: calls.append(pane_id))
    argv = [command]
    if pane_id is not None:
        argv += ["--pane-id", pane_id]

    assert cli.main(argv) == 0
    assert calls == [pane_id]


def test_main_invokes_new_window(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[None] = []
    monkeypatch.setattr(cli, "run_new_window", lambda: calls.append(None))

    assert cli.main(["new-window"]) == 0
    assert calls == [None]
