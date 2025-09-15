from __future__ import annotations

import sys
import types
from io import StringIO
from pathlib import Path
from unittest.mock import Mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

try:  # pragma: no cover - fallback for environments without libtmux
    from libtmux import Server  # type: ignore
    from libtmux.exc import LibTmuxException
except ModuleNotFoundError:  # pragma: no cover - executed only in CI where libtmux missing
    libtmux_module = types.ModuleType("libtmux")

    class Server:  # type: ignore[too-many-ancestors]
        """Minimal stub used when libtmux is unavailable during tests."""

        def cmd(self, *args: object, **kwargs: object) -> None:  # pragma: no cover - not used
            raise NotImplementedError

    exc_module = types.ModuleType("libtmux.exc")

    class LibTmuxException(Exception):
        """Placeholder exception matching the real libtmux hierarchy."""

    exc_module.LibTmuxException = LibTmuxException
    libtmux_module.Server = Server
    libtmux_module.exc = exc_module
    sys.modules["libtmux"] = libtmux_module
    sys.modules["libtmux.exc"] = exc_module

    from libtmux.exc import LibTmuxException  # type: ignore  # noqa: E402

from tmux_quick_tabs.new_window import INITIALIZATION_COMMAND, run_new_window


def make_mock_server():
    return Mock(spec=["cmd"])


def test_run_new_window_with_simple_name():
    server = make_mock_server()
    stdin = StringIO("dev\n")
    stdout = StringIO()

    run_new_window(server=server, stdin=stdin, stdout=stdout)

    server.cmd.assert_any_call("neww", "-n", "dev")
    server.cmd.assert_any_call("send-keys", INITIALIZATION_COMMAND, "Enter")
    assert stdout.getvalue() == "Enter window name:\n"


def test_run_new_window_with_spaces_in_name():
    server = make_mock_server()
    stdin = StringIO("foo bar\n")
    stdout = StringIO()

    run_new_window(server=server, stdin=stdin, stdout=stdout)

    server.cmd.assert_any_call("neww", "-n", "foo", "bar")
    server.cmd.assert_any_call("send-keys", INITIALIZATION_COMMAND, "Enter")


def test_run_new_window_allows_empty_name_and_still_sends_keys():
    server = make_mock_server()
    stdin = StringIO("\n")
    stdout = StringIO()

    server.cmd.side_effect = [LibTmuxException("usage error"), None]

    run_new_window(server=server, stdin=stdin, stdout=stdout)

    assert server.cmd.call_args_list[0].args == ("neww", "-n")
    assert server.cmd.call_args_list[1].args == (
        "send-keys",
        INITIALIZATION_COMMAND,
        "Enter",
    )
