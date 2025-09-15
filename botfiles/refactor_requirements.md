# Refactor Requirements

This document captures the exact behaviour of the current `tmux-quick-tabs` plugin.  The Python/libtmux rewrite must replicate every feature and quirk described below without adding new functionality.

## Core Concepts

- **Hidden tab session**: Each pane tracks a background session used as a tab buffer.  The name is produced with `tabs_<session>_<window>_<pane>` via `tmux display -p "tabs_#S_#W_#P"`.
- **TPM installation**: Must support installation through the tmux plugin manager (`tmux-plugins/tpm`) by adding `set -g @plugin 'meltingshoe/tmux-quick-tabs'`.
- **Tab storage**: Every tab is represented by a window inside the hidden session.  `swap-pane` is used to move panes in and out of this session.

## Key Bindings

Bindings are defined in `qt-binds.tmux` and must be recreated exactly:
- Unbind the default `c` and bind `prefix + c` to a popup running `scripts/new-window.sh`.
- Unbind global `C-n` and bind it to `scripts/next-tab.sh`.
- Unbind global `C-t` and bind it to `scripts/new-tab.sh`.
- Unbind `prefix + C-n` and bind it to `scripts/choose-tab.sh`.
- Unbind `prefix + C-t` and bind it to `scripts/close-tab.sh`.

## Feature Details

### Creating a New Tab (`C-t` without prefix)
1. Determine the tab-group name and current pane id.
2. Ensure the tab-group session exists, creating it detached if missing.
3. Create a detached window in the tab-group and capture its id.
4. Swap the active pane with the new tab-group window.
5. Open a popup that executes `create-tab.sh`.
6. If the tab-group contains at least two windows, rotate them by sequentially swapping `tabs:N` with `tabs:N+1` for `N` in `1..buffer_len-1`, shifting panes left.
7. **Dependencies**:
   - Requires `zoxide` and `fzf` through `create-tab.sh`.

### Cycling to the Next Tab (`C-n` without prefix)
1. Determine tab-group name.
2. If the session does not exist, attempt to create it using `tmux new -d -s` (note the incorrect command; it should be `new-session`).
3. Swap the active pane with `tab_group:1`.
4. If the tab-group contains at least two windows, rotate panes by sequentially swapping `tabs:N` with `tabs:N+1` for `N` in `1..buffer_len-1`, shifting panes left.
5. **Bug**: Using `tmux new` instead of `new-session` means the session may not be created, preventing tab cycling when no tab-group exists.

### Choosing a Tab (`prefix + C-n`)
1. Compute tab-group name.
2. Ensure the tab-group session exists.
3. Invoke `tmux choose-tree -F "#{pane_title} #{pane_current_command} #{pane_current_path}" -f "#{==:#{session_name},$(echo $tab_group)}"` to list only panes from the hidden tab session with each entry showing title, current command, and path.
4. When an entry is selected, execute `swap-pane -t '%%'` to swap with the chosen pane.
5. An unused variable captures `session_name:window_name`, serving no functional purpose.

### Closing a Tab (`prefix + C-t`)
1. Compute tab-group name and active pane id.
2. If the tab-group session is missing, kill the active pane.
3. Otherwise, swap the current pane with `tab_group:1` and then kill `tab_group:1`.
4. **Bug**: The tab-group session is never removed when empty, leaving behind "dead" tabs that accumulate over time.

### Creating a New Window (`prefix + c`)
1. Prompt for a window name and read it from stdin.
2. Create the window with `tmux neww -n <name>`.
3. Send the command `cd $(zoxide query -l | fzf); clear; ls -a` to the new pane.
4. **Limitations**: The script performs no validation; an empty name causes `tmux neww -n` to exit with a usage error, and it assumes `zoxide` and `fzf` are available.

### Popup Tab Initialization (`create-tab.sh`)
1. Executed in a popup after a new tab is created.
2. Sends `cd $(zoxide query -l | fzf); clear; ls -a` to the active pane.
3. Contains commented code for naming tabs which is ignored in practice.

## Known Global Issues

- The README states that deleting tabs and state management "does not work" and often leaves orphaned panes, requiring manual cleanup (e.g., `prefix + C-x`).
- The plugin assumes `zoxide` and `fzf` are installed and does not verify their presence.
- No automated tests or linting are provided; behaviour relies entirely on tmux shell scripts.

These points describe the behaviour the Python/libtmux rewrite must match exactly, including the flawed behaviours, before any future improvements are considered.
