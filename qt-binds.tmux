#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
tmux bind-key T run-shell "$CURRENT_DIR/scripts/tmux_list_plugins.sh"



tmux unbind c
tmux bind c display-popup -E "$CURRENT_DIR/scripts/new-window.sh"

tmux unbind -n C-n
tmux bind-key -n C-n run-shell "$CURRENT_DIR/scripts/next-tab.sh"

tmux unbind n
tmux bind-key n run-shell "$CURRENT_DIR/scripts/new-tab.sh"

tmux unbind C-n
tmux bind-key C-n display-popup "$CURRENT_DIR/scripts/qt-menu.sh"

tmux unbind C-x
tmux bind-key C-x run-shell "$CURRENT_DIR/scripts/reset-buffer.sh"

tmux unbind C-m
tmux bind-key C-m next-window
