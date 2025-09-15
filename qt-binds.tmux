#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PYTHON_BIN="$(tmux show-option -gqv '@quick_tabs_python' 2>/dev/null)"
if [ -z "$PYTHON_BIN" ]; then
  PYTHON_BIN="python3"
fi

shell_escape() {
  printf '%q' "$1"
}

PYTHON_BIN_ESCAPED="$(shell_escape "$PYTHON_BIN")"
SRC_PATH_ESCAPED="$(shell_escape "$CURRENT_DIR/src")"
RUNNER="PYTHONPATH=$SRC_PATH_ESCAPED $PYTHON_BIN_ESCAPED -m tmux_quick_tabs"

tmux unbind c
tmux bind c display-popup -E "$RUNNER new-window"

tmux unbind -n C-n
tmux bind-key -n C-n run-shell "$RUNNER next-tab --pane-id '#{pane_id}'"

tmux unbind -n C-t
tmux bind-key -n C-t run-shell "$RUNNER new-tab --pane-id '#{pane_id}'"

tmux unbind C-n
tmux bind-key C-n run-shell "$RUNNER choose-tab --pane-id '#{pane_id}'"

tmux unbind C-t
tmux bind-key C-t run-shell "$RUNNER close-tab --pane-id '#{pane_id}'"
