# Examples Directory

This directory contains example scripts demonstrating the features of the KHTN-THCS lesson plan generator.

## Available Examples

### latex_word_demo.py

Demonstrates the LaTeX rendering and Word export features:

```bash
python examples/latex_word_demo.py
```

This script shows:
1. **LaTeX Formula Rendering**: How to render mathematical formulas to PNG images
2. **Word Document Export**: How to create Word documents from lesson plan configurations
3. **CLI Usage**: Examples of using the command-line interface

## Running the Examples

### Prerequisites

Make sure you have installed all dependencies:

```bash
pip install -r requirements.txt
```

### Example 1: LaTeX Formula Rendering

```python
from pathlib import Path
from app.latex_renderer import LatexRenderer

# Create a renderer
renderer = LatexRenderer(output_dir=Path("outputs/examples"))

# Render a formula
output_path = renderer.render_to_file("E = mc^2")
print(f"Formula saved to: {output_path}")
```

### Example 2: Word Document Export

```python
from pathlib import Path
from app.word_exporter import export_to_word

# Create a lesson plan configuration
config = {
    "metadata": {
        "title": "My Lesson Plan",
        "grade": "Lớp 8",
    },
    "objectives": ["Objective 1", "Objective 2"],
    "formulas": [
        {
            "symbol": "F",
            "description": "Force",
            "latex": "F = ma"
        }
    ]
}

# Export to Word
export_to_word(config, Path("outputs/my_lesson.docx"))
```

### Example 3: Using the CLI

```bash
# Generate Markdown
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json

# Generate Word document
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json \
  --format word -o outputs/lesson.docx

# Generate both formats
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json \
  --format both -o outputs/lesson.md
```

## Output Files

After running the examples, you will find:

- **outputs/examples/**: Rendered formula images (PNG files)
- **outputs/example_lesson.docx**: Example Word document
- **outputs/formulas/**: Cached formula images used in documents

## More Information

For detailed documentation, see:
- [LaTeX and Word Export Guide](../docs/LATEX_WORD_EXPORT.md)
- [Main README](../README.md)

## Contributing

To add new examples:

1. Create a new Python script in this directory
2. Add proper documentation and comments
3. Test the script to ensure it runs correctly
4. Update this README with information about the new example
