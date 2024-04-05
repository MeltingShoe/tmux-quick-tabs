#!/usr/bin/env bash
echo "Enter window name:"
read input
tmux neww -n $input
