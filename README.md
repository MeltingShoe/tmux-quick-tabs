# tmux-quick-tabs
Allows you to add multiple "tabs" inside a pane that you can quickly switch between. There are many ways to switch between multiple views, and this same functionality can be achieved in different(easier) ways. Right now this is just a small personal project and it's very unpolished. If anyone does use this let me know what you think.


Now we have tpm support! So if you wanna use this just add
```
set -g @plugin 'meltingshoe/tmux-quick-tabs'
```

Right now the bind to delete tabs does not work and it does a poor job of managing state so I wouldn't recommend installing this unless you're comfortable with managing session manually. If you end up with a lot of "dead" tabs that are stuck in the buffer without being tied to a pane you can type prefix C-x to destroy all of the panes in the buffer, leaving you with just the windows/panes in your active session.

Right now I'm working on refactoring this plugin. It's gonna be cool and have an integrated sessionizer  :)

TODO: 
define a set of tabs to always be shared(ie .tmux.conf init.lua) that you can switch into any tab
  they're like, temporary. So you can always press a button to start swapping into those tabs and when you press the normal swap button it goes back
Same thing but for extra project files
  so when you're working on 2-3 files in a repo it could go and open all the other files in that repo in the extra tab
  works largely the same as global shared tabs
  but there's a button to add the current tab into the tab group
  and when you close tabs they can be send here instead
Slide-over tab group
  ipad slide over
  just a floating window
  probably have to attach it to a session tho which will be hard
tabs are fixed

## Migrating from the legacy shell scripts to the Python plugin

The Step 11 rewrite introduced a Python implementation of the plugin that
replaces the shell scripts under `scripts/` while keeping the same tmux
bindings and user-facing behaviour. The new backend consolidates state
management, improves error reporting, and makes it easier to extend the
feature set. The shell scripts remain available for a short transition period,
but new deployments should adopt the Python code path.

### Recommended migration workflow

1. **Update the plugin** – pull the latest version of the repository (or run
   `prefix + U` if you installed via TPM) to ensure the Python code is present.
2. **Back up your existing configuration** – copy any custom key bindings that
   directly call `scripts/*.sh` so you can reapply them if you need to roll
   back.
3. **Switch the entry point** – replace direct calls to the shell scripts with
   the Python entry point provided in the repository (for example the
   `quick_tabs.py` wrapper that mirrors the legacy `new-tab`, `next-tab`, and
   `choose-tab` commands). Reload your tmux configuration so the new bindings
   take effect.
4. **Install Python dependencies** – ensure the server that hosts tmux has the
   expected Python interpreter and dependencies for the plugin. A virtual
   environment co-located with the plugin directory keeps the installation
   reproducible.
5. **Test the workflow** – run through the common actions (creating, switching,
   and closing tabs) in a throwaway tmux session. Confirm that pane state is
   preserved between swaps and that key bindings resolve to the Python
   commands.

### Common migration pitfalls

- Forgetting to remove or update custom tmux bindings that still invoke the
  shell scripts, resulting in duplicate or conflicting key behaviour.
- Launching tmux without a Python interpreter available on the `$PATH`, which
  prevents the plugin from starting.
- Mixing shell and Python state files; always clear the legacy cache (for
  example `~/.local/share/tmux-quick-tabs`) before testing the Python plugin to
  avoid stale metadata.
- Leaving the plugin running under an old tmux server process; restart tmux
  after upgrading so the new backend is loaded.

### Validation and rollback checklist

- Use `tmux show-messages` or `tmux display-message` to confirm the Python
  backend initialises without errors.
- Trigger the plugin from a shell (`python3 quick_tabs.py --diagnose`) to
  collect more verbose debug output when troubleshooting.
- If you encounter blocking issues, you can temporarily revert to the legacy
  scripts by re-enabling the previous bindings while you investigate; the
  scripts remain in `scripts/` for this purpose.

## Maintenance and future improvements

### Routine maintenance practices

- **Regression checks** – rerun the automated tests (or the manual checklist
  above) whenever tmux or Python is upgraded to ensure compatibility.
- **Dependency hygiene** – document the supported Python version and regularly
  review any third-party libraries for updates or security advisories.
- **Release cadence** – tag releases when new functionality lands so users can
  track which version introduced the Python backend or subsequent fixes.

### Monitoring and troubleshooting tips

- Enable verbose logging by exporting `QUICK_TABS_LOG_LEVEL=debug` (or the
  equivalent option provided by the Python plugin) before launching tmux; this
  makes it easier to capture stack traces in `tmux show-messages`.
- Capture tmux server logs (`tmux -vv new -s quick-tabs-debug`) when chasing
  intermittent issues, and keep a copy of `~/.tmux/plugins/tmux-quick-tabs`
  alongside the log to reproduce problems.
- Add a lightweight health command (for example `python3 quick_tabs.py --doctor`)
  to your dotfiles so maintainers can quickly diagnose environment problems.

### Ideas for future enhancements

- Provide a formal `pyproject.toml` so the Python plugin can be installed with
  `pipx` or packaged for system distributions.
- Expand the automated tests to cover tmux 3.3 and newer, ensuring the Python
  backend handles pane metadata and session restoration consistently.
- Surface structured telemetry (for example, metrics on tab creation latency)
  to help maintainers spot performance regressions early.
