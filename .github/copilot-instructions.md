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
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)
```

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
2. **Commit Messages**: Can be in Vietnamese or English, but be descriptive
3. **Testing**: Test generated Markdown files to ensure LaTeX expressions render correctly
4. **Documentation Updates**: Update README.md if adding new features or changing structure
5. **Non-commercial Use**: All materials are for educational purposes, not commercial use

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
