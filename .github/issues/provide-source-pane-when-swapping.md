# Provide source pane when swapping in close tab command

## Summary
The new `close_tab` command swaps the hidden buffer pane into the active tab without specifying a source pane. libtmux does not implicitly select the current pane when commands are executed outside of a tmux client, so `swap-pane -t tab_group_name:1` may target the wrong pane or fail entirely. We need to pass the active pane id (`-s`) when invoking `swap-pane` to ensure the intended pane is swapped.

## Follow-up Tasks
- Update `close_tab.py` to supply the source pane id when calling `swap-pane`.
- Add regression coverage that exercises the command through libtmux to ensure the explicit source pane is required.

## References
- Review suggestion in PR implementing the close tab command (path `src/tmux_quick_tabs/close_tab.py`, line 53).
