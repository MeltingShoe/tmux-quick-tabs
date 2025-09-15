# Project Overview

## Goals and Philosophy
- Provide quick "tab" management inside a single tmux pane for fast context switching.
- Keep the implementation lightweight using shell scripts and native tmux commands.

## Implemented Features
- **Create new tabs** with `C-t` or `new-tab.sh` which swaps the current pane into a background session and opens a prompt to pick a directory using `zoxide` and `fzf`.
- **Cycle to the next tab** using `C-n` through `next-tab.sh`, rotating panes from the background session.
- **Choose from existing tabs** via an interactive tree (`choose-tab.sh`) bound to `C-n`.
- **Close the current tab** with `C-t` (`close-tab.sh`) that replaces it with the next stored pane or kills the pane if no group exists.
- **Create new windows** using `c` (`new-window.sh`) which prompts for a name and starting directory.

## Implementation Details
- Tabs are stored in an off-screen session named using `tabs_<session>_<window>_<pane>` and managed with `swap-pane` and `new-window` calls.
- Scripts rely on external tools `zoxide` and `fzf` to choose working directories.
- Key bindings are defined in `qt-binds.tmux` and override default tmux bindings for tab actions.

## Referenced but Unimplemented Features
- Shared global tabs that can be swapped into any pane.
- Extra project file tabs where recently used files can be added and reused.
- "Slide-over" tab group acting as a floating window similar to iPad's slide over.

## Bugs and Limitations
- README notes that deleting tabs and state management remain unreliable, leading to "dead" tabs.
- Scripts do not handle missing dependencies (`zoxide`, `fzf`) and lack error checking.
- Closing tabs may fail if the background session lacks panes or indices become inconsistent.

## Critiques and Suggestions
- Manage tab sessions more robustly to avoid orphaned panes and improve state handling.
- Replace repeated `swap-pane` loops with `rotate-window` or dedicated buffer management to simplify logic.
- Consider packaging dependency checks or optional fallbacks when `zoxide`/`fzf` are unavailable.
- Provide automated tests or linting (e.g., shellcheck) to improve reliability.
- Expand README with clearer usage instructions and troubleshooting steps.
