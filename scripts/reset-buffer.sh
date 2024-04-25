#!/usr/bin/env bash
tmux kill-session -t "buffer:"
tmux new -d -s "buffer:"
tmux send-keys "cd \$(zoxide query -l | fzf); clear; ls -a" Enter
