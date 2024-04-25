#!/usr/bin/env bash
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

confirm-before -p "kill-pane #P? (y/n)" run-shell "$CURRENT_DIR/scripts/tmux_list_plugins.sh"

