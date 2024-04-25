#!/usr/bin/env bash
tmux has-session -t "buffer:" || tmux new -d -s "buffer:"
active=$(tmux display -p "#S:#W.#P")
buffer_name=$(tmux display -p "buffer_#S_#W_#P")
buffer_windows=$(tmux list-windows -t buffer -F "#W")
pane_target=$(tmux display -p "buffer:$buffer_name.1")
buffer_path=$(tmux display -p "buffer:$buffer_name")

if ! [[ "$buffer_windows" == *"$buffer_name"* ]]; then
	tmux neww -t "buffer:" -n $buffer_name 
	tmux swap-pane -s $active -t $pane_target
	tmux send-keys "cd \$(zoxide query -l | fzf); clear; ls -a" Enter
	tmux swap-pane -s $active -t $pane_target
fi
tmux swap-pane -Z -s $active -t $pane_target

buffer_len=$(tmux list-panes -t $buffer_path | wc -l)
index="1"
if [ "$buffer_len" -gt $index ]; then
	for i in $(seq $index $buffer_len);
	do
		j=$(($i-1))
		tmux swap-pane -s "buffer:$buffer_name.$i" -t "buffer:$buffer_name.$j"
	done
fi
