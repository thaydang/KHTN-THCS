"""Tests for Word export functionality."""

import unittest
from pathlib import Path
import tempfile
import shutil

from app.word_exporter import WordExporter, export_to_word


class WordExporterTests(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for test outputs."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up temporary directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_export_minimal_config(self):
        """Test exporting a minimal lesson plan configuration."""
        config = {
            "metadata": {
                "title": "Bài học thử nghiệm",
                "date": "2024-01-15",
                "grade": "Lớp 7",
            }
        }
        output_path = self.test_dir / "test_minimal.docx"

        exporter = WordExporter(output_dir=self.test_dir)
        exporter.export_lesson_plan(config, output_path)

        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_export_with_objectives_and_materials(self):
        """Test exporting with objectives and materials sections."""
        config = {
            "metadata": {"title": "Bài test"},
            "objectives": ["Mục tiêu 1", "Mục tiêu 2"],
            "materials": ["Máy chiếu", "Thí nghiệm"],
        }
        output_path = self.test_dir / "test_sections.docx"

        exporter = WordExporter(output_dir=self.test_dir)
        exporter.export_lesson_plan(config, output_path)

        self.assertTrue(output_path.exists())

    def test_export_with_formulas(self):
        """Test exporting with LaTeX formulas."""
        config = {
            "metadata": {"title": "Bài có công thức"},
            "formulas": [
                {
                    "symbol": "F",
                    "description": "Lực",
                    "latex": "F = ma",
                },
                {
                    "symbol": "E",
                    "description": "Năng lượng",
                    "latex": "E = mc^2",
                },
            ],
        }
        output_path = self.test_dir / "test_formulas.docx"

        exporter = WordExporter(output_dir=self.test_dir)
        exporter.export_lesson_plan(config, output_path)

        self.assertTrue(output_path.exists())
        # Check that formula images were created
        formula_dir = self.test_dir / "formulas"
        self.assertTrue(formula_dir.exists())
        self.assertGreater(len(list(formula_dir.glob("*.png"))), 0)

    def test_export_with_activities(self):
        """Test exporting with teaching activities."""
        config = {
            "metadata": {"title": "Bài có hoạt động"},
            "activities": [
                {
                    "title": "Khởi động",
                    "duration": "10 phút",
                    "goals": ["Gây hứng thú"],
                    "steps": [
                        {"actor": "Giáo viên", "content": "Giới thiệu bài"},
                        {"actor": "Học sinh", "content": "Thảo luận nhóm"},
                    ],
                    "digital_assets": ["Slide 1-2"],
                }
            ],
        }
        output_path = self.test_dir / "test_activities.docx"

        exporter = WordExporter(output_dir=self.test_dir)
        exporter.export_lesson_plan(config, output_path)

        self.assertTrue(output_path.exists())

    def test_export_with_latex_in_text(self):
        """Test exporting with LaTeX expressions in regular text."""
        config = {
            "metadata": {"title": "Bài có LaTeX trong text"},
            "objectives": [
                "Vận dụng công thức $F = ma$ trong bài tập",
                "Tính được $v = v_0 + at$ khi biết các đại lượng",
            ],
        }
        output_path = self.test_dir / "test_latex_text.docx"

        exporter = WordExporter(output_dir=self.test_dir)
        exporter.export_lesson_plan(config, output_path)

        self.assertTrue(output_path.exists())

    def test_convenience_function(self):
        """Test the convenience export_to_word function."""
        config = {
            "metadata": {"title": "Test convenience"},
            "objectives": ["Objective 1"],
        }
        output_path = self.test_dir / "test_convenience.docx"

        export_to_word(config, output_path)

        self.assertTrue(output_path.exists())

    def test_export_full_lesson_plan(self):
        """Test exporting a complete lesson plan with all sections."""
        config = {
            "metadata": {
                "title": "Bài học đầy đủ",
                "date": "2024-09-05",
                "grade": "Lớp 6",
                "unit": "Chủ đề 2",
                "topic": "Bài 8",
                "teacher": "Nguyễn Văn A",
                "school": "THCS Test",
            },
            "objectives": ["Mục tiêu 1", "Mục tiêu 2"],
            "competencies": ["Năng lực 1", "Năng lực 2"],
            "materials": ["Máy chiếu", "Bộ thí nghiệm"],
            "digital_resources": ["Slide bài giảng", "Video"],
            "formulas": [
                {"symbol": "I", "description": "Cường độ", "latex": r"I = \frac{P}{4\pi r^2}"}
            ],
            "activities": [
                {
                    "title": "Hoạt động 1",
                    "duration": "15 phút",
                    "goals": ["Mục tiêu hoạt động"],
                    "steps": [{"actor": "GV", "content": "Nội dung"}],
                    "digital_assets": ["Tài nguyên"],
                }
            ],
            "assessment": ["Đánh giá 1"],
            "homework": ["Bài tập 1"],
            "reflection": ["Ghi chú"],
        }
        output_path = self.test_dir / "test_full.docx"

        exporter = WordExporter(output_dir=self.test_dir)
        exporter.export_lesson_plan(config, output_path)

        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 5000)  # Should be a reasonable size


if __name__ == "__main__":
    unittest.main()
