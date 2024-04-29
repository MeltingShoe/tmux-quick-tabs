#!/usr/bin/env bash
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#echo "Enter tab name:"
#read input

#tab_group=$(tmux display -p "tabs_#S_#W_#P")
#newid=$(tmux new-window -d -t $tab_group -P )
#echo $input
#tmux select-pane -t $newid -T $input
tmux send-keys "cd \$(zoxide query -l | fzf); clear; ls -a" Enter
