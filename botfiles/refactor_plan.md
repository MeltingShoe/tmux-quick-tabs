# Refactor Execution Plan

### Step 1 — Establish Python project scaffolding
*Dependencies:* none  
Create a new directory structure, `pyproject.toml`, and an entry module (e.g., `tmux_quick_tabs/__init__.py`). Configure linting/formatting hooks and virtual environment.

### Step 2 — Implement tab‑group discovery
*Dependencies:* Step 1  
Use `libtmux` to reproduce `tmux display -p "tabs_#S_#W_#P"` and ensure a detached session named `tabs_<session>_<window>_<pane>` exists (creating it if missing).

### Step 3 — Replicate “create new tab” behavior (`C‑t` without prefix)
*Dependencies:* Step 2  
Port `scripts/new-tab.sh` and `create-tab.sh` logic: create a new window in the hidden session, swap panes, invoke a popup to run the initialization command (`cd $(zoxide query -l | fzf); clear; ls -a`), then rotate hidden windows.

### Step 4 — Replicate “cycle to next tab” (`C‑n` without prefix)
*Dependencies:* Step 2  
Port `scripts/next-tab.sh`: swap the active pane with `tab_group:1`, rotate windows, and mirror the original bug where `tmux new` is used instead of `new-session`.

### Step 5 — Implement “choose tab” tree (`prefix + C‑n`)
*Dependencies:* Step 2  
Port `scripts/choose-tab.sh`: generate the pane list via `choose-tree` filtered by hidden session panes, and swap the chosen pane with the active one.

### Step 6 — Implement “close tab” (`prefix + C‑t`)
*Dependencies:* Step 2  
Port `scripts/close-tab.sh`: swap with `tab_group:1`, kill that pane, and intentionally keep the hidden session alive even when empty.

### Step 7 — Implement “new window” popup (`prefix + c`)
*Dependencies:* Step 1  
Port `scripts/new-window.sh`: prompt for a name, run `tmux neww -n <name>`, and send the `zoxide`/`fzf` initialization command without validation.

### Step 8 — Centralize dependency checks
*Dependencies:* Step 3, Step 4, Step 5, Step 6, Step 7  
Verify presence of `zoxide` and `fzf`; emit warnings if missing but preserve existing behavior otherwise.

### Step 9 — Bind keys and TPM integration
*Dependencies:* Step 3, Step 4, Step 5, Step 6, Step 7  
Provide a `.tmux` configuration snippet mimicking `qt-binds.tmux`; ensure plugin works when added via `set -g @plugin 'meltingshoe/tmux-quick-tabs'`.

### Step 10 — Add automated tests and linting
*Dependencies:* Step 3, Step 4, Step 5, Step 6, Step 7, Step 8, Step 9  
Unit-test each command’s `libtmux` interactions and shell fallbacks; add `shellcheck` for remaining scripts.

### Step 11 — Update documentation
*Dependencies:* Step 10  
Revise README to describe Python version, exact behavior, TPM installation, known limitations, and testing instructions.

### Step 12 — Provide migration and maintenance notes
*Dependencies:* Step 11  
Explain how to transition from shell scripts to Python plugin, outline common pitfalls, and document future improvement ideas.
