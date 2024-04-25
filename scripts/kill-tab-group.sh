#!/usr/bin/env bash



tmux has-session -t "buffer:" || tmux new -d -s "buffer:"
active=$(tmux display -p "#S:#W.#P")
buffer_path=$(tmux display -p "buffer:$buffer_name")

tmux kill-pane -t $buffer_path
if ! [[ "$buffer_windows" == *"$buffer_name"* ]]; then
	tmux neww -t "buffer:" -n $buffer_name
	tmux send-keys "cd \$(zoxide query -l | fzf); clear; ls -a" Enter
fi
