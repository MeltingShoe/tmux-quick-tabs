# Refactor Steps and Agent Prompts

> **Start here:** Before executing any prompt below, read `AGENTS.md` for repository-wide rules, confirm your step and its dependencies in `botfiles/refactor_plan.md`, and review behavioural requirements in `botfiles/refactor_requirements.md`.

## Step 1 — Establish Python project scaffolding
*Dependencies:* none
```
You are working on Step 1 of the tmux-quick-tabs refactor: establish the Python project scaffolding.
Goals:
1. Create the initial Python package layout (pyproject.toml, tmux_quick_tabs package, entry module).
2. Configure linting/formatting hooks and document how to activate the virtual environment.
Requirements:
- Follow guidance in botfiles/refactor_requirements.md.
- Prefer modern Python packaging practices.
Deliverables:
- Scaffolding files committed and ready for subsequent steps.
- Notes on development setup if needed.
```

## Step 2 — Implement tab-group discovery
*Dependencies:* Step 1
```
You are working on Step 2 of the tmux-quick-tabs refactor: implement tab-group discovery and creation.
Goals:
1. Provide a function `get_or_create_tab_group(pane)` returning a detached libtmux Session named `tabs_<session>_<window>_<pane>`.
2. Mirror tmux display formatting logic to derive the session name.
Requirements:
- Create the hidden session if it does not exist.
- Add unit tests verifying session naming and creation behavior.
Deliverables:
- Implementation module.
- Test coverage for success and existing-session cases.
```

## Step 3 — Replicate “create new tab” behavior (`C-t` without prefix)
*Dependencies:* Step 2
```
Implement Step 3: the "create new tab" command.
Goals:
1. Reproduce scripts/new-tab.sh and create-tab.sh behavior using libtmux.
2. Swap panes into the hidden session, open the initialization popup, then rotate hidden windows.
Requirements:
- Fail if zoxide or fzf are missing (to be relaxed later in Step 8).
- Include tests mocking libtmux to confirm rotation and popup invocation.
Deliverables:
- Command implementation.
- Unit tests demonstrating expected tmux calls.
```

## Step 4 — Replicate “cycle to next tab” (`C-n` without prefix)
*Dependencies:* Step 2
```
Implement Step 4: cycle to the next tab.
Goals:
1. Swap the active pane with tab_group:1 and rotate hidden windows.
2. Preserve the original bug where `tmux new` is used instead of `new-session`.
Requirements:
- Handle missing hidden session by creating it with the buggy command.
- Add tests covering present and absent session scenarios.
Deliverables:
- Command implementation.
- Associated unit tests.
```

## Step 5 — Implement “choose tab” tree (`prefix + C-n`)
*Dependencies:* Step 2
```
Implement Step 5: the "choose tab" tree command.
Goals:
1. Use `choose-tree` filtered to panes within the hidden tab session.
2. Swap the selected pane with the active pane in the visible window.
Requirements:
- Match output formatting from scripts/choose-tab.sh.
- Write tests that simulate choose-tree selection and confirm pane swapping.
Deliverables:
- Command implementation.
- Unit tests for selection handling.
```

## Step 6 — Implement “close tab” (`prefix + C-t`)
*Dependencies:* Step 2
```
Implement Step 6: the "close tab" command.
Goals:
1. Swap the active pane with tab_group:1 and kill that pane.
2. Keep the hidden session alive even when no panes remain.
Requirements:
- Mirror the original script behavior exactly, including window rotation semantics.
- Provide tests verifying pane kill operations and session persistence.
Deliverables:
- Command implementation.
- Unit tests for closing behavior.
```

## Step 7 — Implement “new window” popup (`prefix + c`)
*Dependencies:* Step 1
```
Implement Step 7: new-window popup.
Goals:
1. Prompt the user for a window name and run `tmux neww -n <name>`.
2. Send the initialization command from the shell script version without validation.
Requirements:
- Allow empty names to mirror existing failure modes.
- Write tests mocking user input and tmux command execution.
Deliverables:
- Command implementation.
- Associated unit tests.
```

## Step 8 — Centralize dependency checks
*Dependencies:* Step 3, Step 4, Step 5, Step 6, Step 7
```
Implement Step 8: centralized dependency checks.
Goals:
1. Provide a reusable check for zoxide and fzf availability.
2. Emit warnings instead of hard failures while preserving prior behaviors when dependencies are missing.
Requirements:
- Integrate checks into commands from Steps 3–7.
- Add tests ensuring warnings fire correctly and commands still execute when possible.
Deliverables:
- Dependency utility module.
- Updated commands with coverage for dependency scenarios.
```

## Step 9 — Bind keys and TPM integration
*Dependencies:* Step 3, Step 4, Step 5, Step 6, Step 7
```
Implement Step 9: key bindings and TPM integration.
Goals:
1. Provide a tmux configuration snippet equivalent to qt-binds.tmux using the new Python entrypoints.
2. Ensure the plugin functions when installed via TPM (`set -g @plugin 'meltingshoe/tmux-quick-tabs'`).
Requirements:
- Document required key bindings and configuration variables.
- Add tests or scripts validating that bindings invoke the correct commands.
Deliverables:
- Updated tmux configuration assets.
- Documentation or tests demonstrating integration.
```

## Step 10 — Add automated tests and linting
*Dependencies:* Step 3, Step 4, Step 5, Step 6, Step 7, Step 8, Step 9
```
Implement Step 10: automated tests and linting.
Goals:
1. Ensure unit tests cover each command’s libtmux interactions and shell fallbacks.
2. Add tooling such as pytest configuration and shellcheck for remaining scripts.
Requirements:
- Update CI or local automation instructions.
- Provide evidence that tests and linters run successfully.
Deliverables:
- Testing and linting configuration files.
- Documentation updates describing how to run the checks.
```

## Step 11 — Update documentation
*Dependencies:* Step 10
```
Implement Step 11: documentation refresh.
Goals:
1. Revise README to describe the Python implementation, installation, and key bindings.
2. Document testing instructions, known limitations, and environment expectations.
Requirements:
- Reference earlier steps’ outcomes and note preserved quirks.
- Include migration instructions where appropriate.
Deliverables:
- Updated README and any supporting docs.
```

## Step 12 — Provide migration and maintenance notes
*Dependencies:* Step 11
```
Implement Step 12: migration and maintenance notes.
Goals:
1. Explain how to transition from shell scripts to the Python plugin.
2. Outline ongoing maintenance practices and future improvement ideas.
Requirements:
- Highlight common pitfalls encountered during migration.
- Suggest monitoring or troubleshooting tips for maintainers.
Deliverables:
- Migration guide and maintenance notes appended to documentation.
```
