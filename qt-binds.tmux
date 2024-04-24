#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
tmux bind-key T run-shell "$CURRENT_DIR/scripts/tmux_list_plugins.sh"



unbind c
bind c display-popup -E "$CURRENT_DIR/scripts/new-window.sh"

unbind -n C-n
bind-key -n C-n run-shell "$CURRENT_DIR/scripts/next-tab.sh"

unbind n
bind-key n run-shell "$CURRENT_DIR/scripts/new-tab.sh"

unbind C-n
bind-key C-n display-popup "$CURRENT_DIR/scripts/qt-menu.sh"

unbind C-x
bind-key C-x run-shell "$CURRENT_DIR/scripts/reset-buffer.sh"

unbind C-m
bind-key C-m next-window
