# Kho tài liệu Khoa học Tự nhiên THCS - Copilot Instructions

## Project Overview

This repository stores and shares teaching materials for Natural Science (Khoa học Tự nhiên - KHTN) at the middle school level (THCS - Trung học cơ sở). The project includes lesson plans, test materials, virtual experiments, and reference documents organized systematically for teachers and students.

**Target Audience**: Middle school science teachers in Vietnam and their students (grades 6-9).

**Primary Purpose**: Provide a collaborative repository for teachers to build and share curriculum-aligned teaching resources.

## Tech Stack

- **Primary Language**: Python 3
- **Documentation**: Markdown with LaTeX math expressions
- **Document Processing**: 
  - Pandoc for document conversion
  - XeLaTeX for PDF generation
  - JSON for structured lesson plan data
- **Build Tools**: Bash scripts for PDF generation
- **Version Control**: Git/GitHub

## Project Structure

```
.
├── GiaoAn/              # Lesson plans by grade (6, 7, 8, 9)
├── DeKiemTra/           # Test materials (matrices, specs, questions, answers)
├── ThiNghiemAo/         # Virtual experiments (Chemistry, Physics, Biology)
├── TaiLieu/             # Textbooks, official documents, references
├── app/                 # Main lesson plan generator application
│   └── lesson_plan_generator.py
├── tools/
│   ├── lesson_planner/  # Legacy lesson planner
│   └── khtn_ai_editor/  # Pandoc/XeLaTeX templates and build tools
├── samples/             # Example lesson plan configurations (JSON)
├── outputs/             # Generated documents output
└── resources/           # Shared resources
```

## Coding Guidelines

### Python Code

1. **Style**: Follow PEP 8 conventions
2. **Type Hints**: Use type annotations (from `typing` module) for function parameters and return values
3. **Docstrings**: Include module-level and function-level docstrings in English
4. **Encoding**: Always use UTF-8 encoding when reading/writing files with Vietnamese text
5. **Data Classes**: Use `@dataclass` decorator for structured data models
6. **File Handling**: Use `pathlib.Path` for file operations instead of raw strings

### Code Example Pattern

```python
from pathlib import Path
from typing import Dict, Any

def _read_json(path: Path) -> Dict[str, Any]:
    """Read and parse a JSON file.
    
    Args:
        path: Path to the JSON file
        
    Returns:
        Dictionary containing the parsed JSON data
    """
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)
```

### Error Handling

1. **File Operations**: Always handle `FileNotFoundError` and `PermissionError` when working with files
2. **JSON Parsing**: Catch `json.JSONDecodeError` and provide helpful error messages
3. **Validation**: Validate input data before processing, especially for user-provided JSON configurations
4. **Encoding Issues**: Use `encoding="utf-8"` explicitly and handle `UnicodeDecodeError` for Vietnamese text files

### Security Guidelines

1. **No Hardcoded Secrets**: Never commit passwords, API keys, or credentials to the repository
2. **File Paths**: Validate and sanitize file paths to prevent directory traversal attacks
3. **User Input**: Always validate and sanitize user input, especially in JSON configurations
4. **Dependencies**: Keep dependencies minimal; verify packages before adding new ones

### Documentation

1. **Language**: Use Vietnamese for user-facing content (README, comments in lesson plans, generated documents)
2. **Technical Comments**: English is acceptable for code comments
3. **LaTeX Support**: Preserve LaTeX expressions (e.g., `$F = ma$`) in Markdown files for math rendering
4. **File Format**: UTF-8 encoding is mandatory for all text files

## Key Features and Workflows

### Lesson Plan Generator (`app/lesson_plan_generator.py`)

The main tool for generating structured lesson plans from JSON configuration:

```bash
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json -o output.md
```

**Input**: JSON configuration with:
- `metadata`: lesson info (title, date, grade, teacher, school)
- `objectives`: learning objectives
- `competencies`: skills and qualities to develop
- `materials`: required teaching materials
- `digital_resources`: digital learning materials and links
- `formulas`: mathematical formulas with LaTeX expressions
- `activities`: teaching activities with steps
- `assessment`, `homework`, `reflection`: post-lesson sections

**Output**: Structured Markdown document with preserved LaTeX math expressions.

### Important Patterns

1. **LaTeX in JSON**: Use double backslashes (`\\`) in JSON strings to represent LaTeX backslashes:
   ```json
   "latex": "I = \\dfrac{P}{4\\pi r^2}"
   ```

2. **Activity Steps**: Each step has an `actor` (e.g., "Giáo viên", "Học sinh") and `content`

3. **Markdown Sections**: Generated documents follow a consistent structure matching Vietnamese education standards

## Curriculum Alignment

- **Standards**: Aligned with Vietnam's General Education Program 2018 (Chương trình GDPT 2018)
- **Grades**: 6-9 middle school (THCS)
- **Subjects**: Integrated Natural Sciences covering Physics, Chemistry, and Biology
- **Official Documents**: Follow Ministry of Education circulars and guidelines (Công văn Bộ GD&ĐT)

## Common Tasks

### Adding a New Lesson Plan

1. Create a JSON configuration file in `samples/` or appropriate grade folder
2. Follow the structure of existing samples (e.g., `grade6_light_and_shadow.json`)
3. Run the generator: `python app/lesson_plan_generator.py path/to/config.json -o output.md`
4. Review the generated Markdown for formatting and accuracy

### Modifying the Generator

- Edit `app/lesson_plan_generator.py`
- Maintain dataclass structure for `Step` and `Activity`
- Keep functions pure and testable
- Preserve UTF-8 encoding handling

### Building PDF Documents

Use the tools in `tools/khtn_ai_editor/`:
- Templates are in `templates/`
- Build scripts in `scripts/build_pdf.sh`
- Requires Pandoc and XeLaTeX installation

## Testing, Building, and Linting

### Running Tests

**Unit Tests**: Use Python's built-in unittest framework
```bash
# Run all tests
python -m unittest discover -s tests -v

# Run a specific test file
python -m unittest tests.test_lesson_plan_generator -v
```

**Test Requirements**:
- All public functions in `app/` should have corresponding unit tests
- Tests should cover normal cases, edge cases, and error conditions
- Use descriptive test method names that explain what is being tested

### Running the Application

**Lesson Plan Generator**:
```bash
# Basic usage
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json -o output.md

# With custom output location
python app/lesson_plan_generator.py path/to/config.json -o outputs/my_lesson.md
```


### Code Quality

**Style Checking**: Follow PEP 8 conventions. No automated linter is currently configured, but code should:
- Use 4 spaces for indentation (not tabs)
- Keep lines under 100 characters when practical
- Use snake_case for functions and variables
- Use PascalCase for classes

**Manual Validation**:
- Run the application after making changes to ensure it works
- Test with sample JSON files in `samples/` directory
- Verify generated Markdown renders correctly with LaTeX expressions
- Check that UTF-8 Vietnamese text displays properly

## Commit Message Conventions

Follow these guidelines for commit messages:

**Format**:
```
<type>: <subject>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature or functionality
- `fix`: Bug fix
- `docs`: Documentation changes only
- `refactor`: Code refactoring without changing functionality
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build scripts)

**Examples**:
```
feat: add support for multiple formulas in lesson plans

fix: handle missing metadata fields gracefully

docs: update README with timeseries tool usage

refactor: extract JSON validation to separate function

test: add edge case tests for empty activities list
```

**Guidelines**:
- Keep subject line under 72 characters
- Use imperative mood ("add" not "added" or "adds")
- Can be written in English or Vietnamese
- Reference issue numbers if applicable (e.g., "fix #123")

## Vietnamese Language Context

**Common Terms**:
- **Giáo án**: Lesson plan
- **Học liệu**: Learning materials
- **Thí nghiệm**: Experiment
- **Đề kiểm tra**: Test/Exam
- **Giáo viên**: Teacher
- **Học sinh**: Student
- **Năng lực**: Competency/Skill
- **Mục tiêu**: Objective
- **Hoạt động**: Activity

When generating or modifying content, maintain Vietnamese terminology for educational concepts.

## Best Practices for Contributions

1. **File Naming**: Use descriptive names in Vietnamese or English (avoid special characters)
2. **Commit Messages**: Follow the commit message conventions above
3. **Testing**: Test generated Markdown files to ensure LaTeX expressions render correctly
4. **Documentation Updates**: Update README.md if adding new features or changing structure
5. **Non-commercial Use**: All materials are for educational purposes, not commercial use
6. **Code Review**: All changes should be reviewed before merging to main branch

## AI Assistant Guidelines

### When to Ask for Clarification

Always ask clarifying questions when:
- Requirements are ambiguous or incomplete
- Multiple valid approaches exist and the choice impacts the solution significantly
- The task involves modifying critical parts of the codebase (e.g., data validation logic)
- Security implications are unclear
- The request conflicts with existing patterns or best practices
- You're unsure about Vietnamese educational terminology or standards

### Code Generation Expectations

When generating code:
1. **Follow Existing Patterns**: Match the style and structure of existing code
2. **Preserve Functionality**: Don't break existing features unless specifically asked to fix them
3. **Minimal Changes**: Make the smallest change necessary to accomplish the goal
4. **Document Changes**: Add docstrings for new functions, update comments if logic changes
5. **Test Compatibility**: Ensure changes work with existing test suite
6. **Handle Errors Gracefully**: Add appropriate error handling for edge cases

### Good vs Bad Code Examples

**Good - Proper Error Handling**:
```python
def read_lesson_config(path: Path) -> Dict[str, Any]:
    """Read lesson configuration from JSON file."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")
```

**Bad - No Error Handling**:
```python
def read_lesson_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
```

**Good - Type Hints and Docstring**:
```python
def format_duration(minutes: int) -> str:
    """Format duration in minutes to Vietnamese text.
    
    Args:
        minutes: Duration in minutes
        
    Returns:
        Formatted string like "10 phút" or "1 giờ 30 phút"
    """
    if minutes < 60:
        return f"{minutes} phút"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours} giờ {remaining_minutes} phút" if remaining_minutes > 0 else f"{hours} giờ"
```

**Bad - No Type Hints or Documentation**:
```python
def format_duration(m):
    if m < 60:
        return f"{m} phút"
    h = m // 60
    rm = m % 60
    return f"{h} giờ {rm} phút" if rm > 0 else f"{h} giờ"
```

### Validation Before Implementation

Before implementing significant changes:
1. Run existing tests to establish baseline: `python -m unittest discover -s tests -v`
2. Review related code files to understand context
3. Check if similar functionality already exists
4. Verify the change aligns with Vietnamese educational standards if applicable
5. Consider impact on existing lesson plans and generated documents

## Useful Resources

- [Vietnam Education Program 2018](https://moet.gov.vn) - Official curriculum guidelines
- [Markdown Math Support](https://www.mathjax.org/) - For LaTeX expression rendering
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html) - For understanding code structure
- [Pandoc Documentation](https://pandoc.org/) - For document conversion tools

## Notes for AI Assistants

- Respect the bilingual nature: Vietnamese for educational content, English for technical code
- Preserve existing file encoding (UTF-8) when making modifications
- When generating lesson plans, follow Vietnamese educational standards and terminology
- LaTeX expressions in Markdown should remain intact and properly escaped
- Directory structure follows Vietnamese educational organization (by grade, subject area)
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
