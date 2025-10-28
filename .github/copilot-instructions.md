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
    if remaining_minutes == 0:
        return f"{hours} giờ"
    return f"{hours} giờ {remaining_minutes} phút"
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
