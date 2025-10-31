"""Lesson plan generator for Natural Science lesson plans.

This script reads lesson plan data from a JSON configuration file and
produces a Markdown document suitable for sharing as a teaching plan or
digital lesson outline. The generated Markdown keeps LaTeX expressions
intact so they can be rendered by Markdown viewers that support math.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class Step:
    """Represents a single step inside an activity."""

    actor: str
    content: str

    def to_markdown(self, indent: int = 0) -> str:
        bullet = " " * indent + f"- **{self.actor}**: {self.content.strip()}"
        return bullet


@dataclass
class Activity:
    """Represents a teaching activity within the lesson."""

    title: str
    duration: Optional[str] = None
    goals: List[str] = field(default_factory=list)
    steps: List[Step] = field(default_factory=list)
    digital_assets: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines: List[str] = [f"### {self.title}"]
        if self.duration:
            lines.append(f"- **Thời lượng**: {self.duration}")
        if self.goals:
            lines.append("- **Mục tiêu hoạt động**:")
            lines.extend("  - " + goal for goal in self.goals)
        if self.steps:
            lines.append("- **Tiến trình**:")
            lines.extend(step.to_markdown(indent=2) for step in self.steps)
        if self.digital_assets:
            lines.append("- **Học liệu/Bài giảng điện tử**:")
            lines.extend("  - " + asset for asset in self.digital_assets)
        return "\n".join(lines)


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _coerce_steps(raw_steps: Iterable[Dict[str, Any]]) -> List[Step]:
    steps: List[Step] = []
    for step in raw_steps:
        actor = step.get("actor") or "Giáo viên"
        content = step.get("content") or ""
        steps.append(Step(actor=actor, content=content))
    return steps


def _coerce_activities(raw_activities: Iterable[Dict[str, Any]]) -> List[Activity]:
    activities: List[Activity] = []
    for activity in raw_activities:
        steps = _coerce_steps(activity.get("steps", []))
        goals = [goal for goal in activity.get("goals", []) if goal]
        digital_assets = [
            asset for asset in activity.get("digital_assets", []) if asset
        ]
        activities.append(
            Activity(
                title=activity.get("title", "Hoạt động"),
                duration=activity.get("duration"),
                goals=goals,
                steps=steps,
                digital_assets=digital_assets,
            )
        )
    return activities


def _format_bullet_section(title: str, items: Iterable[str]) -> Optional[str]:
    filtered = [item.strip() for item in items if item]
    if not filtered:
        return None
    lines = [f"## {title}"]
    lines.extend(f"- {item}" for item in filtered)
    return "\n".join(lines)


def _format_table_section(
    title: str, rows: Iterable[Dict[str, str]], *, headers: List[str]
) -> Optional[str]:
    rows = [
        row for row in rows if any(row.get(header, "").strip() for header in headers)
    ]
    if not rows:
        return None

    lines = [f"## {title}"]
    header_line = " | ".join(headers)
    divider_line = " | ".join(["---"] * len(headers))
    lines.append(f"{header_line}")
    lines.append(divider_line)
    for row in rows:
        line = " | ".join(row.get(header, "").strip() or "-" for header in headers)
        lines.append(line)
    return "\n".join(lines)


def build_markdown(config: Dict[str, Any]) -> str:
    metadata = config.get("metadata", {})
    title = metadata.get("title") or "Kế hoạch bài dạy Khoa học Tự nhiên"
    lesson_date = metadata.get("date") or date.today().isoformat()
    grade = metadata.get("grade")
    unit = metadata.get("unit")
    topic = metadata.get("topic")
    teacher = metadata.get("teacher")
    school = metadata.get("school")

    lines: List[str] = [f"# {title}"]
    info_pairs = [
        ("Ngày dạy", lesson_date),
        ("Khối lớp", grade),
        ("Chủ đề", unit),
        ("Bài học", topic),
        ("Giáo viên", teacher),
        ("Trường", school),
    ]
    info_text = [f"- **{label}**: {value}" for label, value in info_pairs if value]
    if info_text:
        lines.append("\n".join(info_text))

    objectives = config.get("objectives", [])
    objectives_section = _format_bullet_section("Mục tiêu bài học", objectives)
    if objectives_section:
        lines.append("\n" + objectives_section)

    competencies_section = _format_bullet_section(
        "Năng lực, phẩm chất hình thành", config.get("competencies", [])
    )
    if competencies_section:
        lines.append("\n" + competencies_section)

    materials_section = _format_bullet_section(
        "Học liệu và thiết bị", config.get("materials", [])
    )
    if materials_section:
        lines.append("\n" + materials_section)

    digital_section = _format_bullet_section(
        "Bài giảng điện tử và học liệu số", config.get("digital_resources", [])
    )
    if digital_section:
        lines.append("\n" + digital_section)

    formulas = config.get("formulas", [])
    formula_rows = [
        {
            "Ký hiệu": formula.get("symbol", ""),
            "Diễn giải": formula.get("description", ""),
            "Biểu thức LaTeX": (
                f"${formula.get('latex', '').strip()}$" if formula.get("latex") else ""
            ),
        }
        for formula in formulas
    ]
    formula_section = _format_table_section(
        "Công thức và ký hiệu sử dụng",
        formula_rows,
        headers=["Ký hiệu", "Diễn giải", "Biểu thức LaTeX"],
    )
    if formula_section:
        lines.append("\n" + formula_section)

    activities = _coerce_activities(config.get("activities", []))
    if activities:
        lines.append("\n## Tiến trình dạy học")
        for activity in activities:
            lines.append("\n" + activity.to_markdown())

    assessment_section = _format_bullet_section(
        "Đánh giá", config.get("assessment", [])
    )
    if assessment_section:
        lines.append("\n" + assessment_section)

    homework_section = _format_bullet_section(
        "Hướng dẫn học tập tiếp theo", config.get("homework", [])
    )
    if homework_section:
        lines.append("\n" + homework_section)

    reflection_section = _format_bullet_section(
        "Ghi chú và tự đánh giá", config.get("reflection", [])
    )
    if reflection_section:
        lines.append("\n" + reflection_section)

    return "\n\n".join(lines) + "\n"


def generate_markdown(config_path: Path, output_path: Path) -> None:
    config = _read_json(config_path)
    markdown = build_markdown(config)
    output_path.write_text(markdown, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tạo kế hoạch bài dạy/bài giảng điện tử môn Khoa học Tự nhiên ở định dạng Markdown."
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Đường dẫn tới tệp JSON mô tả kế hoạch bài dạy.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Đường dẫn tệp Markdown đầu ra. Mặc định cùng thư mục với tệp cấu hình.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path: Path = args.config
    output_path: Path = args.output or config_path.with_suffix(".md")

    if not config_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp cấu hình: {config_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_markdown(config_path, output_path)
    print(f"✅ Đã tạo kế hoạch bài dạy tại: {output_path}")


if __name__ == "__main__":
    main()
