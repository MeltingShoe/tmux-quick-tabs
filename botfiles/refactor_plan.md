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

---

## Agent Prompts

**Generic structure for each agent**  
```
You are working on <Step X> from the tmux-quick-tabs refactor.
Goals:
1. <summary of step>
2. Preserve existing quirks described in botfiles/refactor_requirements.md.
Requirements:
- Use Python + libtmux (or shell where specified).
- Follow repo style and instructions.
- Output only final files/commands; no extra commentary.
Deliverables:
- Code implementing the feature.
- Updated tests/documentation if relevant.
```

### Example Prompts

1. **Step 2 Agent (Tab-group discovery)**
   ```
   You are working on Step 2 of the tmux-quick-tabs refactor: implement tab-group discovery and creation.
   - Expose a function `get_or_create_tab_group(pane)` that returns a libtmux Session named `tabs_<session>_<window>_<pane>`.
   - Must create the session detached if it does not exist.
   - Add unit tests verifying session naming.
   ```

2. **Step 3 Agent (Create new tab)**
   ```
   Implement Step 3: the "create new tab" command.
   - Reproduce scripts/new-tab.sh and create-tab.sh behavior.
   - Swap panes into the hidden session, open a popup to run the init command, then rotate hidden windows.
   - Fail if zoxide/fzf are missing (dependency check in Step 8 will later relax this).
   - Include tests that mock libtmux and confirm the rotation.
   ```

3. **Step 4 Agent (Cycle to next tab)**
   ```
   Implement Step 4: cycle to the next tab.
   - Swap the active pane with tab_group:1 and rotate.
   - Reproduce the existing bug where 'tmux new' is used instead of 'new-session'.
   - Provide tests showing behavior when the session is absent.
   ```

4. **Step 7 Agent (New window popup)**
   ```
   Implement Step 7: new-window popup.
   - Prompt user for a window name; run 'tmux neww -n <name>'.
   - Send the initialization command and allow empty name (preserving failure behavior).
   - Write tests mocking user input and command execution.
   ```

(Continue generating prompts for remaining steps similarly.)

---

## Orchestrating Multiple Agents

### Dependency Graph Highlights
- **Root:** Step 1 must complete before any other step.
- **Early Parallelism:**  
  After Step 2 finishes, Steps 3–6 can run in parallel since they all depend on tab-group logic but not on each other.  
  Step 7 can begin once Step 1 is done (independent of Step 2).
- **Integration Phase:**  
  Step 8 waits for Steps 3–7.  
  Step 9 depends on Steps 3–7 as well but can run concurrently with Step 8.  
  Step 10 requires Steps 3–9 to be finished.  
  Step 11 waits on tests (Step 10), and Step 12 follows documentation updates.

### Suggested Orchestration
1. **Agent A:** complete Step 1 → spawn Agent B for Step 2 and Agent C for Step 7 simultaneously.
2. **Agent B:** once Step 2 done, spawn Agents D–G for Steps 3–6 in parallel.
3. **Agents D–G + C:** once all finish, spawn Agents H (Step 8) and I (Step 9) concurrently.
4. **Agent J:** after H and I complete, handle Step 10.
5. **Agent K:** proceed with Step 11.
6. **Agent L:** finalize with Step 12.

This orchestration allows maximum concurrency while respecting dependencies. A single agent could instead follow the numbered steps sequentially.

---

## Execution Notes
- Each agent should reference `botfiles/refactor_requirements.md` to match existing behavior.
- Encourage agents to write unit tests early (within their step) to reduce integration issues later.
- Use a shared issue tracker or checklist to mark completion and unblock dependent tasks.
