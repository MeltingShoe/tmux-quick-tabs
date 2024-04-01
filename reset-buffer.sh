#!/usr/bin/env bash
tmux kill-session -t "buffer:"
tmux new -d -s "buffer:"
