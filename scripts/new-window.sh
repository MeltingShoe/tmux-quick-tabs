#!/usr/bin/env bash
echo "Enter window name:"
read input
tmux neww -n $input
tmux send-keys "cd \$(zoxide query -l | fzf); cls; ls -a" Enter
