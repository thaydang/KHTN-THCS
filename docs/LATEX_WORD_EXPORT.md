# LaTeX Rendering and Word Export Features

This document explains the new features for rendering LaTeX formulas as images and exporting lesson plans to Word format.

## Overview

Two new features have been added to the KHTN-THCS lesson plan generator:

1. **LaTeX Formula Rendering**: Convert LaTeX mathematical expressions to PNG images using Matplotlib
2. **Word Export**: Export lesson plans to Microsoft Word (.docx) format with embedded formula images

## LaTeX Formula Rendering

### Module: `app/latex_renderer.py`

The `LatexRenderer` class uses Matplotlib to render LaTeX formulas as high-quality PNG images.

### Features

- **High Resolution**: Renders at 300 DPI for print quality
- **Transparent Background**: Images have transparent backgrounds for easy embedding
- **Smart Caching**: Identical formulas are cached to avoid re-rendering
- **Error Handling**: Provides clear error messages for invalid LaTeX expressions

### Usage

#### Basic Usage

```python
from app.latex_renderer import LatexRenderer
from pathlib import Path

# Create a renderer
renderer = LatexRenderer(output_dir=Path("outputs/formulas"))

# Render a formula to file
output_path = renderer.render_to_file("E = mc^2")
print(f"Formula saved to: {output_path}")

# Render to bytes (for in-memory use)
image_bytes = renderer.render_to_bytes("F = ma")
```

#### Convenience Functions

```python
from app.latex_renderer import render_latex_to_file, render_latex_to_bytes

# Direct file rendering
render_latex_to_file("a^2 + b^2 = c^2", Path("formula.png"))

# Direct bytes rendering
image_data = render_latex_to_bytes(r"\dfrac{P}{4\pi r^2}")
```

### Supported LaTeX

The renderer uses Matplotlib's built-in LaTeX parser (mathtext), which supports:

- Basic math operators: `+`, `-`, `*`, `/`, `=`
- Superscripts: `x^2`, subscripts: `H_2O`
- Fractions: `\frac{a}{b}`, `\dfrac{a}{b}`
- Greek letters: `\alpha`, `\beta`, `\pi`, etc.
- Common math symbols: `\sum`, `\int`, `\sqrt{x}`
- Operators: `\sin`, `\cos`, `\tan`, `\log`
- And many more standard LaTeX math commands

Note: This uses Matplotlib's mathtext parser, not full LaTeX, so some advanced LaTeX features may not be supported.

## Word Export

### Module: `app/word_exporter.py`

The `WordExporter` class converts lesson plan configurations to Microsoft Word (.docx) format.

### Features

- **Full Lesson Plan Support**: All sections (metadata, objectives, activities, etc.)
- **Embedded Formula Images**: LaTeX formulas are automatically rendered and embedded
- **Vietnamese Font Support**: Uses Times New Roman with proper Vietnamese character support
- **Professional Formatting**: Consistent headings, bullets, and tables
- **Formula Tables**: Special handling for formula sections with images

### Usage

#### Basic Usage

```python
from app.word_exporter import export_to_word
from pathlib import Path
import json

# Load lesson plan configuration
with open("lesson_plan.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Export to Word
export_to_word(config, Path("lesson_plan.docx"))
```

#### Using the WordExporter Class

```python
from app.word_exporter import WordExporter

exporter = WordExporter(output_dir=Path("outputs"))
exporter.export_lesson_plan(config, Path("my_lesson.docx"))
```

### LaTeX in Text

LaTeX expressions in regular text (e.g., in objectives or steps) are automatically detected and rendered:

```json
{
  "objectives": [
    "Vận dụng được công thức $F = ma$ trong bài tập",
    "Tính được tốc độ $v = v_0 + at$ khi biết các đại lượng"
  ]
}
```

These formulas will be rendered as small inline images in the Word document.

## Command Line Interface

### Updated `lesson_plan_generator.py`

The CLI now supports multiple output formats:

```bash
# Generate Markdown (default)
python app/lesson_plan_generator.py config.json -o output.md

# Generate Word document
python app/lesson_plan_generator.py config.json --format word -o output.docx

# Generate both formats
python app/lesson_plan_generator.py config.json --format both -o output.md
```

### Options

- `--format {markdown,word,both}`: Choose output format (default: markdown)
- `-o, --output`: Specify output file path
- `--render-formulas`: (Reserved for future use) Force formula rendering

### Examples

```bash
# Example 1: Generate Word document
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json \
  --format word -o outputs/lesson_plan.docx

# Example 2: Generate both Markdown and Word
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json \
  --format both -o outputs/lesson_plan.md

# Example 3: Default Markdown output
python app/lesson_plan_generator.py samples/grade6_light_and_shadow.json
```

## Configuration Format

The lesson plan JSON format remains unchanged. LaTeX formulas should be specified in the `latex` field of formula objects:

```json
{
  "formulas": [
    {
      "symbol": "I",
      "description": "Cường độ ánh sáng tại vị trí quan sát",
      "latex": "I = \\dfrac{P}{4\\pi r^2}"
    }
  ]
}
```

**Important**: In JSON, backslashes must be escaped (use `\\` instead of `\`).

## Dependencies

The new features require additional Python packages:

```bash
pip install -r requirements.txt
```

Required packages:
- `matplotlib>=3.7.0` - For LaTeX rendering
- `pillow>=10.0.0` - Image processing
- `python-docx>=0.8.11` - Word document creation
- `markdown>=3.4.0` - Markdown parsing utilities

## Testing

Comprehensive tests are provided:

```bash
# Run LaTeX renderer tests
python -m unittest tests.test_latex_renderer -v

# Run Word exporter tests
python -m unittest tests.test_word_exporter -v

# Run all tests
python -m unittest discover -s tests -v
```

## Performance

- **Formula Caching**: Identical formulas are cached, so rendering is fast after the first time
- **On-Demand Rendering**: Formulas are only rendered when needed
- **Image Quality**: 300 DPI provides excellent quality for both screen and print

## Troubleshooting

### Import Errors

If you get import errors when running the script:

```bash
# Make sure you're in the project root directory
cd /path/to/KHTN-THCS

# Install dependencies
pip install -r requirements.txt

# Run the script from the project root
python app/lesson_plan_generator.py ...
```

### LaTeX Rendering Errors

If a LaTeX formula fails to render:

1. Check that the formula is valid LaTeX math syntax
2. Remember to escape backslashes in JSON (`\\` not `\`)
3. The renderer uses Matplotlib's mathtext parser, not full LaTeX
4. Check the error message for hints about what went wrong

### Word Document Issues

If the Word document doesn't open correctly:

1. Make sure python-docx is installed: `pip install python-docx`
2. Check that the output directory exists and is writable
3. Try opening the file with LibreOffice if MS Word has issues

## Future Enhancements

Possible future improvements:

1. **PDF Generation with Embedded Images**: Integrate rendered formulas into PDF workflow
2. **Custom Styling**: Allow users to customize Word document styles
3. **MathML Support**: Add MathML export for better accessibility
4. **Batch Processing**: Process multiple lesson plans at once
5. **Template Support**: Allow custom Word templates

## Contributing

To contribute improvements:

1. Follow the existing code style (PEP 8)
2. Add tests for new features
3. Update this documentation
4. Ensure all tests pass before submitting

## License

This feature is part of the KHTN-THCS project and follows the same license terms.
