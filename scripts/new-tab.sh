#!/usr/bin/env bash
tmux has-session -t "buffer:" || tmux new -d -s "buffer:"
active=$(tmux display -p "#S:#W.#P")
buffer_name=$(tmux display -p "buffer_#S_#W_#P")
buffer_windows=$(tmux list-windows -t buffer -F "#W")
buffer_path=$(tmux display -p "buffer:$buffer_name")
pane_target=$(tmux display -p "buffer:$buffer_name.1")
pane_source=$(tmux display -p "buffer:$buffer_name.1")

if ! [[ "$buffer_windows" == *"$buffer_name"* ]]; then
	tmux neww -c -t "buffer:" -n $buffer_name
	tmux swap-pane -s $active -t $pane_target
	tmux send-keys "cd \$(zoxide query -l | fzf); cls; ls -a" Enter
fi

buffer_len=$(tmux list-panes -t $buffer_path | wc -l)
tar_len=$(($buffer_len + 1))
dest_path=$(tmux display -p "buffer:$buffer_name.$tar_len")
last_path=$(tmux display -p "buffer:$buffer_name.$buffer_len")

tmux split-window -c "#{pane_current_path}" -t "$last_path"
tmux swap-pane -s "$dest_path" -t "$active"
tmux send-keys "cd \$(zoxide query -l | fzf);cls;ls -a" Enter
