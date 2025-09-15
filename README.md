# tmux-quick-tabs
Allows you to add multiple "tabs" inside a pane that you can quickly switch between. There are many ways to switch between multiple views, and this same functionality can be achieved in different(easier) ways. Right now this is just a small personal project and it's very unpolished. If anyone does use this let me know what you think.


Now we have tpm support! So if you wanna use this just add
```
set -g @plugin 'meltingshoe/tmux-quick-tabs'
```

## Key bindings

The tmux plugin installs the following bindings when sourced by TPM:

* `prefix + c` opens a popup that runs the Python entrypoint `tmux-quick-tabs new-window`.
* `C-n` (no prefix) runs `tmux-quick-tabs next-tab` to cycle to the next stored pane.
* `C-t` (no prefix) runs `tmux-quick-tabs new-tab` to create a new tab and open the popup prompt.
* `prefix + C-n` runs `tmux-quick-tabs choose-tab` to display a filtered `choose-tree`.
* `prefix + C-t` runs `tmux-quick-tabs close-tab` to swap the current pane into the hidden session and kill it.

These commands map directly to the Python modules in `src/tmux_quick_tabs` and mirror the legacy shell scripts.

### Configuration options

The plugin looks for the tmux option `@quick_tabs_python` to determine which Python interpreter to use. If the option is unset,
`python3` is used. Example:

```
set -g @quick_tabs_python "/usr/bin/python3.11"
```

The entrypoints set `PYTHONPATH` to the plugin's `src` directory so they can run when the repository is cloned by TPM without a
separate installation step.

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

## Development setup

The Python rewrite lives in the `src/tmux_quick_tabs` package and is distributed via
`pyproject.toml`.  To work on the refactor you can create an isolated environment and
install the editable project plus development tools:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pre-commit install
```

The `pre-commit` hooks format and lint the codebase with [Ruff](https://github.com/astral-sh/ruff)
whenever you commit changes.  Run them manually with `pre-commit run --all-files` when needed.

When the virtual environment is active your shell prompt should include `(.venv)`.  Deactivate
it with `deactivate` once you finish hacking.

You can inspect the placeholder CLI with:

```bash
python -m tmux_quick_tabs --version
```

Future steps in the refactor will flesh out the Python package to replace the shell scripts
shipped with this repository today.
