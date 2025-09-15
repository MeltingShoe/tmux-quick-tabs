# Git History Summary

- **ffd5bab**: Initial commit with minimal README introducing tmux-quick-tabs.
- **431d481**: Added early scripts (`new-tab`, `next-tab`, `close-tab`, etc.) using a shared `buffer` session and basic key bindings.
- **2e4eac1**: Restructured repository for TPM compatibility, moving scripts into a `scripts` directory and updating binds to use relative paths.
- **4855e2c**: Introduced `qt-binds.tmux` for plugin management, added new-window prompts, and integrated `zoxide`/`fzf` directory selection.
- **c1b7a07**: Added pane-killing functionality and a `kill-tab-group` utility.
- **0ea9b08**: Major refactor replacing the `buffer` session approach with per-pane tab groups (`tabs_<session>_<window>_<pane>`), added `choose-tab.sh`, and simplified close/new-tab logic to reduce flicker.
- Subsequent merges polished key bindings, fixed flicker issues, and updated README, culminating in the current lightweight shell-based plugin.
