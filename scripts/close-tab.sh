#!/usr/bin/env bash
tab_group=$(tmux display -p "tabs_#S_#W_#P")
active=$(tmux display -p "#{pane_id}")
tmux has-session -t $tab_group 
if [ $? != 0 ]; then
	tmux kill-pane -t "$active" 
else
	tmux swap-pane -t $tab_group:1 
	tmux kill-pane -t $tab_group:1
fi
