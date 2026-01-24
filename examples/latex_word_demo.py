#!/usr/bin/env python3
"""
Example script demonstrating LaTeX rendering and Word export features.

This script shows how to:
1. Render LaTeX formulas to PNG images
2. Export lesson plans to Word format
3. Use the lesson plan generator with different output formats
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.latex_renderer import LatexRenderer, render_latex_to_file
from app.word_exporter import export_to_word
from app.lesson_plan_generator import _read_json

def example_latex_rendering():
    """Example: Render LaTeX formulas to images."""
    print("Example 1: LaTeX Formula Rendering")
    print("=" * 60)
    
    # Create a renderer
    renderer = LatexRenderer(output_dir=Path("outputs/examples"))
    
    # Example formulas
    formulas = [
        ("Newton's Second Law", "F = ma"),
        ("Light Intensity", r"I = \dfrac{P}{4\pi r^2}"),
        ("Einstein's Mass-Energy", "E = mc^2"),
        ("Velocity Formula", r"v = v_0 + at"),
    ]
    
    print("\nRendering formulas:")
    for name, formula in formulas:
        output_path = renderer.render_to_file(formula)
        print(f"  ✓ {name:25s}: {output_path.name}")
    
    print("\nFormula images saved to: outputs/examples/")
    print()


def example_word_export():
    """Example: Export a lesson plan to Word format."""
    print("Example 2: Word Document Export")
    print("=" * 60)
    
    # Create a simple lesson plan configuration
    config = {
        "metadata": {
            "title": "Bài học ví dụ: Định luật Newton",
            "date": "2024-01-23",
            "grade": "Lớp 8",
            "unit": "Chủ đề 1: Lực và chuyển động",
            "topic": "Bài 3: Định luật II Newton",
            "teacher": "Giáo viên Thí nghiệm",
            "school": "THCS Mẫu",
        },
        "objectives": [
            "Hiểu và vận dụng định luật II Newton: $F = ma$",
            "Tính được gia tốc khi biết lực và khối lượng",
        ],
        "formulas": [
            {
                "symbol": "F",
                "description": "Lực tác dụng (Newton)",
                "latex": "F = ma",
            },
            {
                "symbol": "a",
                "description": "Gia tốc (m/s²)",
                "latex": r"a = \dfrac{F}{m}",
            },
        ],
        "activities": [
            {
                "title": "Khởi động",
                "duration": "10 phút",
                "steps": [
                    {
                        "actor": "Giáo viên",
                        "content": "Đặt câu hỏi về mối liên hệ giữa lực và gia tốc",
                    },
                    {
                        "actor": "Học sinh",
                        "content": "Thảo luận nhóm và trả lời",
                    },
                ],
            }
        ],
    }
    
    # Export to Word
    output_path = Path("outputs/example_lesson.docx")
    export_to_word(config, output_path)
    
    print(f"\n  ✓ Word document created: {output_path}")
    print(f"    File size: {output_path.stat().st_size / 1024:.1f} KB")
    print()


def example_cli_usage():
    """Example: Using the CLI to generate documents."""
    print("Example 3: CLI Usage")
    print("=" * 60)
    
    print("\nCommand line examples:")
    print()
    print("1. Generate Markdown (default):")
    print("   python app/lesson_plan_generator.py config.json")
    print()
    print("2. Generate Word document:")
    print("   python app/lesson_plan_generator.py config.json --format word")
    print()
    print("3. Generate both Markdown and Word:")
    print("   python app/lesson_plan_generator.py config.json --format both")
    print()
    print("4. Specify output path:")
    print("   python app/lesson_plan_generator.py config.json -o outputs/lesson.docx")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("KHTN-THCS: LaTeX Rendering & Word Export Examples")
    print("=" * 60)
    print()
    
    # Run examples
    example_latex_rendering()
    example_word_export()
    example_cli_usage()
    
    print("=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)
    print()
    print("For more information, see: docs/LATEX_WORD_EXPORT.md")
    print()


if __name__ == "__main__":
    main()
