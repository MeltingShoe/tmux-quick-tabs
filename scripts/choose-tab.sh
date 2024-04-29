#!/usr/bin/env bash
tab_group=$(tmux display -p "tabs_#S_#W_#P")
current=$(tmux display -p "#{session_name}:#{window_name}")
tmux has-session -t $tab_group || tmux new-session -d -s $tab_group
tmux choose-tree -F "#{pane_title} #{pane_current_command} #{pane_current_path}" -f "#{==:#{session_name},$(echo $tab_group)}" "swap-pane -t '%%'"
