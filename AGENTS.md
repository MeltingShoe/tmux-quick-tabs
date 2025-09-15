# Agent Handbook for `tmux-quick-tabs`

Welcome! This file provides the shared context every agent needs before working in this repository.

## 1. Get Oriented Before You Start
1. **Read this file in full** to understand repository-wide expectations.
2. **Open `botfiles/refactor_plan.md`** and locate your step to understand its scope, dependencies, and sequencing. Respect the dependency order—if a prerequisite step is incomplete, complete or coordinate on that first.
3. **Review your exact instructions in `botfiles/prompts.md`**. Follow the goals, requirements, and deliverables listed for your step.
4. **Study `botfiles/refactor_requirements.md`**. It documents the canonical behaviour, quirks, and bugs from the existing shell implementation that the Python/libtmux rewrite must replicate.
5. **Inspect the legacy shell scripts in `scripts/` and `qt-binds.tmux`** when you need behavioural references. They are the ground truth for tmux interactions until your Python replacement is complete.

## 2. General Implementation Guidance
- Use Python + `libtmux` for new functionality unless your step explicitly keeps shell code.
- Match the existing user-facing behaviour exactly, including intentional quirks and bugs described in the requirements document.
- Keep code modular so later steps (dependency checks, bindings, documentation, tests) can integrate cleanly.
- When introducing new modules, place them under the future `tmux_quick_tabs/` package created in Step 1 and organise related tests under `tests/` (also created in Step 1).
- Prefer readable, well-documented code (type hints, docstrings where helpful) and reuse shared utilities introduced by earlier steps.

## 3. Quality & Testing Expectations
- Add or update automated tests as part of your step when feasible. Use `pytest` for Python tests and `shellcheck` for shell scripts once those tools are configured.
- **Run every test or check you add or modify** before finishing your task. If a check cannot run (e.g., missing tool), document why in your summary.
- Ensure formatting/linting commands configured in the project (once available) pass before completion.

## 4. Documentation & Configuration
- Update README or other documentation whenever your changes affect user-visible behaviour or setup instructions.
- Keep `botfiles/prompts.md` and `botfiles/refactor_plan.md` consistent with the actual project state if you make structural changes that affect future steps.
- When modifying tmux configuration or shell behaviour, mirror the existing comments and style so users can trace changes easily.

## 5. Communication Back to the Maintainer
- Summarise what changed and reference the tests you ran in your final response.
- Highlight any follow-up work needed for later steps (e.g., if you add TODO markers or identify blocked dependencies).

Following these guidelines ensures every agent has the same context and that the refactor proceeds smoothly across all steps.
