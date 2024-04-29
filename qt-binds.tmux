#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


tmux unbind c
tmux bind c display-popup -E "$CURRENT_DIR/scripts/new-window.sh"

tmux unbind -n C-n
tmux bind-key -n C-n run-shell "$CURRENT_DIR/scripts/next-tab.sh"

tmux unbind -n C-t
tmux bind-key -n C-t run-shell "$CURRENT_DIR/scripts/new-tab.sh"

tmux unbind C-n
tmux bind-key C-n run-shell "$CURRENT_DIR/scripts/choose-tab.sh"

tmux unbind C-t
tmux bind-key C-t run-shell "$CURRENT_DIR/scripts/close-tab.sh"


