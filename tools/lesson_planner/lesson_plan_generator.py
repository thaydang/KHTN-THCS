"""Lesson plan generator for Natural Sciences (KHTN) lesson plans.

This module provides a command line application that can build lesson plan
markdown files either from a JSON configuration or via an interactive prompt.
The output markdown is ready for use as lesson plans or e-learning slide
outlines, and it supports LaTeX syntax inside sections (e.g. $F = ma$).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List, Optional


@dataclass
class Activity:
    """Represents a teaching activity within the lesson."""

    phase: str
    description: str
    time_allocation: Optional[str] = None
    notes: Optional[str] = None

    def to_markdown(self) -> str:
        bullet = f"- **{self.phase}**: {self.description.strip()}"
        details: List[str] = []
        if self.time_allocation:
            details.append(f"⌛ {self.time_allocation}")
        if self.notes:
            details.append(f"📝 {self.notes.strip()}")
        if details:
            bullet += f" ({'; '.join(details)})"
        return bullet


@dataclass
class LessonPlan:
    """Internal representation of a Natural Sciences lesson plan."""

    title: str
    grade_level: str
    topic: str
    duration: str
    author: Optional[str] = None
    objectives: List[str] = field(default_factory=list)
    materials: List[str] = field(default_factory=list)
    activities: List[Activity] = field(default_factory=list)
    assessments: List[str] = field(default_factory=list)
    homework: Optional[str] = None
    references: List[str] = field(default_factory=list)
    notes: Optional[str] = None

    def to_markdown(self) -> str:
        """Render the lesson plan as a Markdown document."""

        sections: List[str] = [f"# {self.title}"]
        header_lines = [
            f"- **Khối lớp:** {self.grade_level}",
            f"- **Chủ đề:** {self.topic}",
            f"- **Thời lượng:** {self.duration}",
        ]
        if self.author:
            header_lines.append(f"- **Người biên soạn:** {self.author}")
        sections.append("\n".join(header_lines))

        if self.objectives:
            sections.append("## Mục tiêu học tập\n" + _to_bullet_list(self.objectives))

        if self.materials:
            sections.append("## Thiết bị và học liệu\n" + _to_bullet_list(self.materials))

        if self.activities:
            activity_lines = "\n".join(activity.to_markdown() for activity in self.activities)
            sections.append("## Hoạt động dạy học\n" + activity_lines)

        if self.assessments:
            sections.append("## Đánh giá\n" + _to_bullet_list(self.assessments))

        if self.homework:
            sections.append("## Bài tập về nhà\n" + self.homework.strip())

        if self.references:
            sections.append("## Tư liệu tham khảo\n" + _to_bullet_list(self.references))

        if self.notes:
            sections.append("## Ghi chú\n" + self.notes.strip())

        return "\n\n".join(sections) + "\n"


def _to_bullet_list(items: List[str]) -> str:
    """Render a list of strings as Markdown bullet points."""

    return "\n".join(f"- {item.strip()}" for item in items)


def load_plan_from_json(path: Path) -> LessonPlan:
    """Load the lesson plan configuration from a JSON file."""

    with path.open(encoding="utf-8") as fp:
        data = json.load(fp)
    return lesson_plan_from_dict(data)


def lesson_plan_from_dict(data: Dict[str, Any]) -> LessonPlan:
    """Create a :class:`LessonPlan` from a dictionary."""

    activities = [
        Activity(
            phase=activity["phase"],
            description=activity["description"],
            time_allocation=activity.get("time_allocation"),
            notes=activity.get("notes"),
        )
        for activity in data.get("activities", [])
    ]

    plan = LessonPlan(
        title=data["title"],
        grade_level=data["grade_level"],
        topic=data["topic"],
        duration=data["duration"],
        author=data.get("author"),
        objectives=data.get("objectives", []),
        materials=data.get("materials", []),
        activities=activities,
        assessments=data.get("assessments", []),
        homework=data.get("homework"),
        references=data.get("references", []),
        notes=data.get("notes"),
    )
    return plan


def interactive_builder() -> LessonPlan:
    """Interactively gather lesson plan information from the user."""

    print("Nhập thông tin kế hoạch bài dạy KHTN. Để trống và nhấn Enter nếu không áp dụng.")
    title = _prompt_required("Tiêu đề bài dạy")
    grade_level = _prompt_required("Khối lớp")
    topic = _prompt_required("Chủ đề/Chương")
    duration = _prompt_required("Thời lượng (ví dụ: 45 phút)")
    author = input("Người biên soạn: ").strip() or None

    objectives = _prompt_list("Mục tiêu học tập (nhập từng mục tiêu, Enter trống để kết thúc)")
    materials = _prompt_list("Thiết bị/học liệu")

    activities: List[Activity] = []
    print("\nNhập các hoạt động dạy học (để trống tên pha để kết thúc).")
    while True:
        phase = input("Pha hoạt động (VD: Khởi động, Hình thành kiến thức...): ").strip()
        if not phase:
            break
        description = _prompt_required("Mô tả hoạt động")
        time_allocation = input("Thời lượng dự kiến: ").strip() or None
        notes = input("Ghi chú (có thể chứa LaTeX): ").strip() or None
        activities.append(
            Activity(
                phase=phase,
                description=description,
                time_allocation=time_allocation,
                notes=notes,
            )
        )

    assessments = _prompt_list("Hình thức đánh giá")
    homework_input = input("Bài tập về nhà (có thể chứa LaTeX): ").strip()
    homework = homework_input or None
    references = _prompt_list("Tài liệu tham khảo")
    notes_input = input("Ghi chú chung: ").strip()
    notes = notes_input or None

    return LessonPlan(
        title=title,
        grade_level=grade_level,
        topic=topic,
        duration=duration,
        author=author,
        objectives=objectives,
        materials=materials,
        activities=activities,
        assessments=assessments,
        homework=homework,
        references=references,
        notes=notes,
    )


def _prompt_required(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("Giá trị này là bắt buộc, vui lòng nhập lại.")


def _prompt_list(label: str) -> List[str]:
    print(label)
    items: List[str] = []
    while True:
        value = input("- ").strip()
        if not value:
            break
        items.append(value)
    return items


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tạo kế hoạch bài dạy Khoa học Tự nhiên và xuất Markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """\
            Ví dụ sử dụng:
              python lesson_plan_generator.py --from-json vi_du.json output.md
              python lesson_plan_generator.py --interactive ke_hoach.md
            """
        ),
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Đường dẫn file Markdown đầu ra.",
    )
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--from-json",
        type=Path,
        help="Đường dẫn tới file JSON mô tả kế hoạch bài dạy.",
    )
    source_group.add_argument(
        "--interactive",
        action="store_true",
        help="Kích hoạt chế độ nhập liệu từng bước trong terminal.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    if args.from_json:
        plan = load_plan_from_json(args.from_json)
    else:
        plan = interactive_builder()

    markdown = plan.to_markdown()
    args.output.write_text(markdown, encoding="utf-8")
    print(f"Đã ghi kế hoạch bài dạy vào {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
