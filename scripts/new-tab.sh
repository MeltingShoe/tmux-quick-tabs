#!/usr/bin/env bash
tab_group=$(tmux display -p "tabs_#S_#W_#P")
active=$(tmux display -p "#{pane_id}")
tmux has-session -t $tab_group || tmux new-session -d -s $tab_group
newid=$(tmux new-window -d -t $tab_group -P )

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
tmux swap-pane -s $active -t $newid
tmux display-popup -E "$CURRENT_DIR/create-tab.sh"

buffer_len=$(tmux list-windows -t $tab_group | wc -l)
index="1"
if [ "$buffer_len" -gt $index ]; then
	for i in $(seq $index $(($buffer_len-1)));
	do
		j=$(($i+1))
		tmux swap-pane -s "$tab_group:$i" -t "$tab_group:$j"
	done
fi

