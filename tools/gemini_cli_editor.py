"""Gemini-powered CLI helper for editing repository files.

This script provides helper commands that call Gemini models through the
`google-generativeai` SDK.  It is designed to streamline content editing
workflows by letting you request plans or full rewrites for project files.

Usage examples:

    # Show a plan for updating the lesson plan generator
    python tools/gemini_cli_editor.py plan "Tạo thêm ví dụ về nhiệt học" \
        --files app/lesson_plan_generator.py docs/TIMESERIES_GUIDE.md

    # Rewrite a Markdown file using Gemini and apply the result automatically
    python tools/gemini_cli_editor.py edit docs/guide.md \
        --instruction "Tóm tắt nội dung ngắn gọn hơn" --apply
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Iterable

import google.generativeai as genai


DEFAULT_MODEL = "gemini-1.5-flash"


def configure(api_key: str | None) -> None:
    """Configure the Gemini SDK with the provided API key."""
    if not api_key:
        raise SystemExit(
            "Gemini API key không được tìm thấy. Đặt biến môi trường GEMINI_API_KEY "
            "hoặc truyền --api-key." 
        )
    genai.configure(api_key=api_key)


def read_files(paths: Iterable[str], max_chars: int) -> str:
    """Read multiple files and return a truncated concatenation."""
    pieces: list[str] = []
    remaining = max_chars
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            pieces.append(f"<FILE path=\"{raw_path}\">Không tìm thấy tệp.</FILE>")
            continue
        
        if remaining <= 0:
            break
            
        # Read file efficiently: only read what we need
        with path.open("r", encoding="utf-8") as f:
            text = f.read(remaining)
        
        remaining -= len(text)
        pieces.append(f"<FILE path=\"{raw_path}\">\n{text}\n</FILE>")
    return "\n".join(pieces)


def call_model(prompt: str, model_name: str, system_instruction: str | None = None) -> str:
    """Call Gemini model and return the plain text response."""
    model = genai.GenerativeModel(model_name, system_instruction=system_instruction)
    response = model.generate_content(prompt)
    return response.text or ""


def command_plan(args: argparse.Namespace) -> int:
    configure(args.api_key)
    context = read_files(args.files, args.max_chars)
    system_instruction = (
        "Bạn là trợ lý phát triển phần mềm hỗ trợ chỉnh sửa tài liệu môn KHTN. "
        "Hãy cung cấp kế hoạch từng bước rõ ràng, nhắc lại tệp nào cần sửa và lý do."
    )
    prompt = "\n".join(
        [
            "<TASK>",
            args.prompt,
            "</TASK>",
            "",
            "<CONTEXT>",
            context or "(Không có tệp nào được cung cấp)",
            "</CONTEXT>",
        ]
    )
    result = call_model(prompt, args.model, system_instruction)
    print(result)
    return 0


CODE_BLOCK_PATTERN = re.compile(r"```(?:[a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)


def extract_code_block(text: str) -> str | None:
    match = CODE_BLOCK_PATTERN.search(text)
    if match:
        return match.group(1).strip()
    return None


def command_edit(args: argparse.Namespace) -> int:
    configure(args.api_key)
    target = Path(args.target)
    if not target.exists():
        raise SystemExit(f"Không tìm thấy tệp: {target}")

    original = target.read_text(encoding="utf-8")
    system_instruction = (
        "Bạn là trợ lý chỉnh sửa nội dung. Khi được yêu cầu 'edit', hãy trả về toàn bộ "
        "nội dung tệp mới trong một code fence Markdown."
    )
    prompt = "\n".join(
        [
            "<EDIT_REQUEST>",
            args.instruction,
            "</EDIT_REQUEST>",
            "",
            "<ORIGINAL_FILE path=\"{}\">".format(args.target),
            original,
            "</ORIGINAL_FILE>",
            "",
            "Hãy xuất bản nội dung tệp đã chỉnh sửa trong code fence dạng ```<ngon_ngu>```.",
        ]
    )
    result = call_model(prompt, args.model, system_instruction)
    candidate = extract_code_block(result)
    if not candidate:
        raise SystemExit(
            "Không tìm thấy code fence trong phản hồi. Hãy kiểm tra lại yêu cầu hoặc phản hồi của mô hình."
        )

    if args.apply:
        target.write_text(candidate, encoding="utf-8")
        print(f"✅ Đã cập nhật {args.target}")
    else:
        print(candidate)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gemini CLI hỗ trợ chỉnh sửa repo KHTN-THCS")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("GEMINI_API_KEY"),
        help="API key dùng cho Gemini. Có thể đặt qua biến môi trường GEMINI_API_KEY.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Tên mô hình Gemini (mặc định: {DEFAULT_MODEL}).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser(
        "plan", help="Sinh kế hoạch chỉnh sửa dựa trên prompt và danh sách tệp."
    )
    plan_parser.add_argument("prompt", help="Mô tả yêu cầu chỉnh sửa hoặc mục tiêu.")
    plan_parser.add_argument(
        "--files",
        nargs="*",
        default=(),
        help="Danh sách tệp làm ngữ cảnh cho mô hình.",
    )
    plan_parser.add_argument(
        "--max-chars",
        type=int,
        default=12000,
        help="Giới hạn ký tự đọc từ các tệp ngữ cảnh.",
    )
    plan_parser.set_defaults(func=command_plan)

    edit_parser = subparsers.add_parser(
        "edit", help="Yêu cầu Gemini viết lại toàn bộ nội dung một tệp."
    )
    edit_parser.add_argument("target", help="Đường dẫn tệp cần chỉnh sửa.")
    edit_parser.add_argument(
        "--instruction",
        required=True,
        help="Hướng dẫn chỉnh sửa chi tiết cho Gemini.",
    )
    edit_parser.add_argument(
        "--apply",
        action="store_true",
        help="Ghi đè tệp bằng nội dung trả về từ Gemini. Nếu không, chỉ in ra màn hình.",
    )
    edit_parser.set_defaults(func=command_edit)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
