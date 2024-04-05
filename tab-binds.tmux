#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

tmux unbind -n C-n
tmux bind-key -n C-n run-shell "${CURRENT_DIR}/scripts/next-tab.sh"

tmux unbind n
tmux bind-key n run-shell "${CURRENT_DIR}/scripts/new-tab.sh"

tmux unbind C-n
tmux bind-key C-n run-shell "${CURRENT_DIR}/scripts/close-tab.sh"

tmux unbind C-x
tmux bind-key C-x run-shell "${CURRENT_DIR}/scripts/reset-buffer.sh"

tmux unbind c
tmux bind c display-popup -d "#{pane_current_path}" -E "${CURRENT_DIR}/scripts/new-window.sh"
