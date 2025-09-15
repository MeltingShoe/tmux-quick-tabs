# tmux-quick-tabs

A tmux plugin that emulates browser-style tabs inside a single pane.  Each tab is
implemented as a hidden tmux window that can be swapped in and out instantly.  The
current refactor rewrote the original shell scripts in Python using
[`libtmux`](https://github.com/tmux-python/libtmux) so the behaviour from the legacy
implementation (Steps&nbsp;2–7 of the plan) is preserved while gaining test coverage and
installability improvements from Steps&nbsp;8–10.

## Overview

- Every active pane owns a detached session named `tabs_<session>_<window>_<pane>` that
  stores its hidden tab windows, matching the shell implementation captured in the
  refactor requirements.
- Python entrypoints under `tmux_quick_tabs/` mirror the `scripts/*.sh` commands and are
  invoked by TPM bindings defined in `qt-binds.tmux` (Step&nbsp;9).
- Optional dependency checks warn about missing `zoxide` or `fzf` (Step&nbsp;8) but never
  abort the command so the preserved shell quirks remain visible.
- The automated tests from Step&nbsp;10 exercise the libtmux interactions for each command;
  see [Development & testing](#development--testing) for instructions.

## Installation

### Install with TPM

Add the plugin to your TPM list and install it with `prefix + I`:

```tmux
set -g @plugin 'meltingshoe/tmux-quick-tabs'
```

TPM will clone the repository and source `qt-binds.tmux`, which wires the Python CLI
into tmux key bindings.

### Manual installation

Clone the repository and source the binding script from your `~/.tmux.conf`:

```tmux
set -g @plugin 'tmux-plugins/tpm'          # if you still use TPM for other plugins
run-shell "~/bin/tmux-quick-tabs/qt-binds.tmux"
```

Adjust the path to match the clone location (for example
`~/.tmux/plugins/tmux-quick-tabs/qt-binds.tmux`).  The binding script configures
tmux to call the Python entrypoints and sets `PYTHONPATH` so the package imports work
without a separate installation step.

### Configure the Python interpreter

The bindings honour the optional `@quick_tabs_python` setting to choose which Python
interpreter runs the commands:

```tmux
set -g @quick_tabs_python "/usr/bin/python3.11"
```

When the option is unset, `python3` is used.  Ensure the interpreter you select has
`libtmux` available so the commands can run.

## Key bindings

The plugin installs the following bindings when `qt-binds.tmux` is sourced:

- `prefix + c` – open a popup that prompts for a window name and runs `tmux-quick-tabs new-window`.
- `C-n` (no prefix) – cycle to the next stored tab via `tmux-quick-tabs next-tab`.
- `C-t` (no prefix) – capture the current pane as a hidden tab with `tmux-quick-tabs new-tab`.
- `prefix + C-n` – list hidden tabs in a filtered `choose-tree` using `tmux-quick-tabs choose-tab`.
- `prefix + C-t` – swap the active pane into the hidden session and kill it with `tmux-quick-tabs close-tab`.

## Command behaviour and preserved quirks

### Hidden tab sessions

`tab_groups.py` mirrors `tmux display -p "tabs_#S_#W_#P"` to derive the detached session
used for storage.  Sessions are created on demand and left running, matching the shell
behaviour described in the requirements.

### `C-t` — create a new tab

`new_tab.py` creates a detached window in the hidden session, swaps it with the active
pane, opens a popup, and rotates the hidden buffer so the newest pane ends up last.
The popup executes `cd $(zoxide query -l | fzf); clear; ls -a`, so both dependencies
should be on `PATH`.  When they are missing the command emits the Step&nbsp;8 warnings but
continues running.

### `C-n` — cycle to the next tab

`next_tab.py` swaps the active pane into `tabs_*:1` and rotates the hidden session.  The
implementation intentionally invokes `tmux new -d -s` instead of `new-session`,
preserving the historical bug where the session might not be created if it is missing.
The swap is attempted regardless so failures mirror the original experience.

### `prefix + C-n` — choose a tab

`choose_tab.py` ensures the hidden session exists and launches `choose-tree` filtered to
`tabs_*` panes.  Each entry shows the pane title, current command, and path exactly like
the shell script, and the `swap-pane` action is triggered when you pick an entry.

### `prefix + C-t` — close the current tab

`close_tab.py` swaps the active pane with `tabs_*:1`, kills the stored pane, and leaves
the hidden session alive even when empty.  This matches the shell leak described in the
plan, so you may need to destroy stray `tabs_*` sessions manually when cleaning up.

### `prefix + c` — create a new window

`new_window.py` prompts for a name, reproduces shell-style word splitting, and then runs
`tmux neww -n <name>`.  Failures from `tmux neww` are ignored so the initialisation
command (`cd $(zoxide query -l | fzf); clear; ls -a`) is still sent, matching the legacy
behaviour and its lack of validation.

## Dependencies & environment

- **tmux:** The popup workflow requires tmux 3.2 or newer for `display-popup`.
- **Python:** The project targets Python 3.9+ (see `pyproject.toml`).
- **libtmux:** Version 0.28 or newer must be installed in the interpreter specified by
  `@quick_tabs_python`.
- **Optional tools:** `zoxide` and `fzf` power the popup initialisation flow.  Missing
  tools trigger warnings but the commands still execute.
- **Environment variables:** When you invoke the CLI outside of tmux you must provide
  `--pane-id`; otherwise the commands fall back to `$TMUX_PANE` like the original scripts.

## Known limitations

- Cycling to the next tab may fail to create the hidden session because the preserved
  `tmux new` call does not behave like `new-session`.
- Closing tabs leaves the hidden session running, so orphaned `tabs_*` sessions can
  accumulate and require manual cleanup (for example with `tmux kill-session -t <name>`).
- The popup initialisation still assumes `zoxide` and `fzf` are installed; the Step&nbsp;8
  warnings highlight the issue but do not provide fallbacks.
- The new-window popup forwards whatever name you enter to `tmux neww -n` without
  validation, so blank names reproduce the original usage error from tmux.

## Development & testing

### Local development environment

Create an isolated environment, install the editable project, and set up the formatting
hooks introduced during the refactor:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pre-commit install
```

`pre-commit` runs Ruff formatting and linting whenever you commit.  Activate the virtual
environment whenever you work on the plugin so `libtmux` and the dev tools are available.

### Running checks

The automated tests and linting from Step&nbsp;10 cover the Python rewrite and the
remaining shell scripts.  Run them with:

```bash
pytest
pre-commit run --all-files
shellcheck scripts/*.sh
```

## Migration from the shell scripts

If you previously bound the shell scripts directly, replace those bindings with a call to
`qt-binds.tmux` so tmux executes the Python CLI instead.  The shell scripts remain in
`scripts/` as references, but the new bindings drive the tested Python modules and keep
behaviour identical to the legacy implementation.  Ensure the Python interpreter you
select via `@quick_tabs_python` has `libtmux`, `zoxide`, and `fzf` available so the popup
initialisation succeeds.  Existing key sequences stay the same, so the upgrade does not
require relearning muscle memory.

Implement Step 12: migration and maintenance notes.
Goals:
1. Explain how to transition from shell scripts to the Python plugin.
2. Outline ongoing maintenance practices and future improvement ideas.
Requirements:
- Highlight common pitfalls encountered during migration.
- Suggest monitoring or troubleshooting tips for maintainers.
Deliverables:
- Migration guide and maintenance notes appended to documentation.
