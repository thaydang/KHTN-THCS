import unittest
from datetime import date

from app.lesson_plan_generator import build_markdown


class BuildMarkdownTests(unittest.TestCase):
    def test_metadata_and_sections_rendered(self) -> None:
        config = {
            "metadata": {
                "title": "Bài học thử nghiệm",
                "date": "2024-01-15",
                "grade": "Lớp 7",
                "unit": "Chủ đề 3",
                "topic": "Bài 5",
                "teacher": "Thầy A",
                "school": "THCS B",
            },
            "objectives": ["Hiểu hiện tượng", "Vận dụng công thức"],
            "competencies": ["Tự học", "Hợp tác"],
            "materials": ["Máy chiếu"],
            "digital_resources": ["Video minh họa"],
            "activities": [
                {
                    "title": "Hoạt động 1",
                    "duration": "10 phút",
                    "goals": ["Khởi động"],
                    "steps": [
                        {"actor": "Giáo viên", "content": "Giới thiệu bài"},
                        {"actor": "Học sinh", "content": "Thảo luận"},
                    ],
                    "digital_assets": ["Slide 1-2"],
                }
            ],
            "assessment": ["Câu hỏi nhanh"],
            "homework": ["Ôn tập"],
            "reflection": ["Điều chỉnh tiến độ"],
        }

        markdown = build_markdown(config)

        self.assertIn("# Bài học thử nghiệm", markdown)
        self.assertIn("- **Ngày dạy**: 2024-01-15", markdown)
        self.assertIn("## Mục tiêu bài học", markdown)
        self.assertIn("- **Tiến trình**:", markdown)
        self.assertIn("### Hoạt động 1", markdown)
        self.assertIn("- **Thời lượng**: 10 phút", markdown)
        self.assertIn("- **Học liệu/Bài giảng điện tử**:", markdown)
        self.assertIn("## Đánh giá", markdown)
        self.assertTrue(markdown.endswith("\n"))

    def test_formula_table_contains_latex(self) -> None:
        config = {
            "formulas": [
                {
                    "symbol": "F",
                    "description": "Lực",
                    "latex": "F = m \\times a",
                }
            ]
        }

        markdown = build_markdown(config)

        self.assertIn("## Công thức và ký hiệu sử dụng", markdown)
        self.assertIn("F = m \\times a", markdown)
        self.assertIn("$F = m \\times a$", markdown)

    def test_defaults_when_metadata_missing(self) -> None:
        markdown = build_markdown({})

        today_text = date.today().isoformat()
        self.assertIn("# Kế hoạch bài dạy Khoa học Tự nhiên", markdown)
        self.assertIn(today_text, markdown)
        self.assertNotIn("## Tiến trình dạy học", markdown)


if __name__ == "__main__":
    unittest.main()
