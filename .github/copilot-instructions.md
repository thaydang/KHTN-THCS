# Copilot Coding Agent Onboarding — KHTN-THCS

Purpose
-------
This file orients a Copilot coding agent to the KHTN-THCS repository so it can make correct, buildable, and reviewable code changes quickly. Follow these instructions as authoritative — search the repo only when something below is incomplete or contradicted by files (for example, CI workflows).

High-level summary
------------------
- What the repo does: A collaborative repository of middle‑school Natural Science (Khoa học Tự nhiên - THCS) teaching materials and tools. Primary use is to generate lesson plans, tests, virtual experiments, and produce documents (Markdown → PDF) using Pandoc + XeLaTeX.
- Project type & stack: Python 3 application plus Markdown/LaTeX templating and Bash build scripts. Small-to-medium repository (mostly docs + Python generators). Main languages: Python, HTML, TeX, Shell.
- Important build/runtime tools: Python 3.10+ (3.8+ acceptable), Pandoc (>=2.11 recommended), TeXLive/XeLaTeX (xetex), Bash, git. Use UTF‑8 everywhere.

Build & validation (always follow in order)
-------------------------------------------
1. Prepare environment (always):
   - Create and activate a virtualenv:
     - python3 -m venv .venv
     - source .venv/bin/activate
   - Always ensure the shell uses UTF-8 (LANG environment).
2. Install Python dependencies:
   - Preferred: pip install -r requirements.txt
   - If requirements.txt is located under app/: pip install -r app/requirements.txt
   - If the repo has no requirements file, install commonly used tools for development:
     - pip install black flake8 pytest
3. Lint & format (always run before tests/commit):
   - Format: python -m black .
   - Lint: python -m flake8 .
   - Enforce type hints where present; run mypy if repo contains a mypy config.
4. Run unit/integration tests (if present):
   - python -m pytest -q
   - If tests are missing, run a quick smoke test: run the main generator on a sample (see below).
5. Smoke test generator (quick local validation):
   - Example:
     - python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json -o outputs/grade6_light_and_shadow.md
     - Then build PDF:
       - pandoc outputs/grade6_light_and_shadow.md -o outputs/grade6_light_and_shadow.pdf --pdf-engine=xelatex
   - If specialized build scripts exist under tools/khtn_ai_editor/scripts, prefer them:
     - bash tools/khtn_ai_editor/scripts/build_pdf.sh outputs/grade6_light_and_shadow.md
6. CI and workflows:
   - Inspect .github/workflows/*.yml (if present) and replicate steps locally. Typical checks: lint, format, smoke generation, PDF build. If a workflow uses specific matrix versions, use the same versions locally.

Build tool versions & notes
---------------------------
- Python: target 3.10+. If repository CI pins a different minor version, match CI.
- Pandoc: >= 2.11 (some templates rely on modern pandoc). On Ubuntu: sudo apt install pandoc
- TeX: Install TeX Live with xetex (texlive-xetex, texlive-latex-extra). PDF builds will fail without xetex.
- Timeouts: PDF builds with large templates/images can take tens of seconds to a few minutes; CI timeouts may be strict — minimize heavy image processing in tests.

Common pitfalls & mitigations
----------------------------
- UTF-8 issues: Always open/write files with encoding="utf-8" and use pathlib.Path for paths.
- LaTeX escaping: JSON fields use double backslashes for LaTeX (e.g., "\\dfrac"). Preserve these when generating Markdown.
- Missing requirements: If requirements.txt is absent, check app/ and tools/ for requirements or a Pipfile; otherwise install minimal dev tools.
- Pandoc/XeLaTeX not installed in CI: If a PR changes PDF generation, ensure workflow installs TeXLive (CI execution time increases).
- Long-running PDF builds: avoid building PDFs in unit tests; use a smoke-target that builds a minimal document.
- File permissions: Bash scripts in tools may need chmod +x.

Project layout & key files
--------------------------
Top-level (priority order)
- app/
  - lesson_plan_generator.py — main generator (entrypoint). Use this for smoke tests and to understand JSON → Markdown logic.
  - (possible app/requirements.txt)
- samples/ — JSON lesson plan examples (use these for tests)
- outputs/ — generated outputs (not committed, ignore)
- tools/
  - khtn_ai_editor/ — Pandoc/XeLaTeX templates and build scripts
    - templates/ — Pandoc/xelatex templates
    - scripts/ — build scripts (build PDF, helper scripts)
  - lesson_planner/ — legacy planner tools
- GiaoAn/, DeKiemTra/, ThiNghiemAo/, TaiLieu/ — content folders (lesson plans, tests, virtual labs, references)
- README.md — repository overview and usage guidance
- .github/workflows/ — CI definitions (lint/test/build jobs)

What to inspect before coding
-----------------------------
1. Open app/lesson_plan_generator.py: understand dataclasses, JSON schema, and outputs.
2. Check samples/ to pick a representative JSON for testing.
3. Review tools/khtn_ai_editor/templates to see Pandoc metadata and required YAML fields.
4. Check .github/workflows/*.yml to replicate CI steps (Python version, commands, matrix).
5. If making changes that affect doc output, update templates and add a smoke test that builds one sample.

Checks to run before creating a PR
---------------------------------
- Run formatting and lint.
- Run unit tests (pytest).
- Run smoke generator on at least one sample and confirm it produces Markdown without encoding/LaTeX errors.
- If you modify PDF generation, run a local PDF build with pandoc + xelatex.
- Ensure new files are UTF-8 encoded.
- Update README or samples if adding new top-level options to generator.

Agent behavior guidance
-----------------------
- Prefer making minimal, well-tested changes in a single PR. Each PR should include a smoke test or instructions to reproduce the change locally.
- For bulk changes across many content files, break into small PRs to avoid long CI runs.
- Trust this file as the primary onboarding resource. Only grep/search the repo when this file lacks detail for the requested change (e.g., a missing workflow or test).
- Add/adjust CI workflow only when necessary and replicate local steps exactly.

If you encounter contradictions (CI vs local)
--------------------------------------------
- Open the relevant .github/workflows YAML and follow its specified Python and tool versions.
- If CI installs extra system packages (e.g., TeXLive) that local machine lacks, add instructions in the PR about required system packages.

Contact / authorship hints
--------------------------
- The repository stores Vietnamese user-facing content — preserve Vietnamese wording and LaTeX syntax. Use English for code comments if needed.
- When in doubt about pedagogical content, make structural/formatting changes only; avoid altering pedagogical text without confirmation.

End of instructions.
