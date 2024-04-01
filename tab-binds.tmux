#!/usr/bin/env bash
tmux unbind -n C-n
tmux bind-key -n C-n run-shell "bash ~/.tmux/plugins/tmux-quick-tabs/next-tab.sh"

tmux unbind n
tmux bind-key n run-shell "bash ~/.tmux/plugins/tmux-quick-tabs/new-tab.sh"

tmux unbind C-n
tmux bind-key C-n run-shell "bash ~/.tmux/plugins/tmux-quick-tabs/close-tab.sh"

tmux unbind C-x
tmux bind-key C-x run-shell "bash ~/.tmux/plugins/tmux-quick-tabs/reset-buffer.sh"

tmux unbind c
tmux bind c display-popup -d "#{pane_current_path}" -E "bash ~/.tmux/plugins/tmux-quick-tabs/new-window.sh"
