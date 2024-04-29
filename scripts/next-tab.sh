#!/usr/bin/env bash
tab_group=$(tmux display -p "tabs_#S_#W_#P")
tmux has-session -t $tab_group || tmux new -d -s $tab_group
active=$(tmux display -p "#{pane_id}")

tmux swap-pane -s $active -t $tab_group:1

buffer_len=$(tmux list-windows -t $tab_group | wc -l)
index="1"
if [ "$buffer_len" -gt $index ]; then
	for i in $(seq $index $(($buffer_len-1)));
	do
		j=$(($i+1))
		tmux swap-pane -s "$tab_group:$i" -t "$tab_group:$j"
	done
fi

